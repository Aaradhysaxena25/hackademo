"""
Integration tests for the full indexing pipeline.
"""

import os
import tempfile

import pytest
from django.contrib.auth import get_user_model

from apps.core.enums import IndexingStatus, RepositoryStatus
from apps.embeddings.models import CodeChunk
from apps.indexing.models import IndexedFile, IndexingJob
from apps.indexing.tasks import index_repository_task
from apps.repositories.models import Repository, RepositoryFile

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="test@example.com",
        email="test@example.com",
        password="TestPass123!",
    )


@pytest.fixture
def repository(user):
    return Repository.objects.create(
        owner=user,
        name="test-project",
        source_type="upload",
        status="pending",
    )


@pytest.fixture
def sample_repo_dir():
    """Create a temporary directory with sample source files."""
    tmpdir = tempfile.mkdtemp(prefix="codepilot_test_")

    # Create Python files
    os.makedirs(os.path.join(tmpdir, "src"))
    with open(os.path.join(tmpdir, "src", "main.py"), "w") as f:
        f.write('''"""Main module."""

def main():
    """Entry point."""
    print("Hello, CodePilot!")
    return 0


def helper(x, y):
    """Add two numbers."""
    return x + y


class App:
    """Main application class."""

    def __init__(self, name):
        self.name = name

    def run(self):
        """Run the application."""
        print(f"Running {self.name}")
''')

    with open(os.path.join(tmpdir, "src", "utils.py"), "w") as f:
        f.write('''"""Utility functions."""

import os
import sys


def read_file(path):
    """Read a file and return its contents."""
    with open(path, "r") as f:
        return f.read()


def write_file(path, content):
    """Write content to a file."""
    with open(path, "w") as f:
        f.write(content)
''')

    # Create a JS file
    with open(os.path.join(tmpdir, "src", "app.js"), "w") as f:
        f.write('''function initialize() {
    console.log("Initializing...");
}

const processData = (data) => {
    return data.map(item => item.value);
}
''')

    # Create README
    with open(os.path.join(tmpdir, "README.md"), "w") as f:
        f.write("# Test Project\n\nA test project for indexing.\n")

    # Create files that should be excluded
    os.makedirs(os.path.join(tmpdir, "node_modules", "pkg"))
    with open(os.path.join(tmpdir, "node_modules", "pkg", "index.js"), "w") as f:
        f.write("module.exports = {}")

    os.makedirs(os.path.join(tmpdir, ".git"))
    with open(os.path.join(tmpdir, ".git", "config"), "w") as f:
        f.write("[core]")

    yield tmpdir

    # Cleanup
    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.mark.django_db
class TestIndexingPipeline:
    """Integration tests for the full indexing pipeline."""

    def test_full_indexing_pipeline(self, repository, sample_repo_dir):
        """Test the complete indexing flow from parse to chunks."""
        # Run the indexing task synchronously (no Celery)
        index_repository_task(str(repository.id), sample_repo_dir)

        # Verify repository was updated
        repository.refresh_from_db()
        assert repository.status == RepositoryStatus.READY
        assert repository.total_files == 4  # main.py, utils.py, app.js, README.md
        assert repository.total_chunks > 0
        assert repository.last_indexed_at is not None
        assert "python" in repository.languages

    def test_indexing_creates_files(self, repository, sample_repo_dir):
        """Test that RepositoryFile records are created."""
        index_repository_task(str(repository.id), sample_repo_dir)

        files = RepositoryFile.objects.filter(repository=repository)
        assert files.count() == 4

        python_files = files.filter(language="python")
        assert python_files.count() == 2

    def test_indexing_creates_chunks(self, repository, sample_repo_dir):
        """Test that code chunks are created for Python functions."""
        index_repository_task(str(repository.id), sample_repo_dir)

        chunks = CodeChunk.objects.filter(repository=repository)
        assert chunks.count() > 0

        # Should have function chunks from Python files
        function_chunks = chunks.filter(chunk_type="function")
        assert function_chunks.count() >= 2  # main, helper, read_file, write_file

    def test_indexing_creates_job(self, repository, sample_repo_dir):
        """Test that an IndexingJob is created and completed."""
        index_repository_task(str(repository.id), sample_repo_dir)

        job = IndexingJob.objects.filter(repository=repository).first()
        assert job is not None
        assert job.status == IndexingStatus.COMPLETED
        assert job.total_files == 4
        assert job.processed_files == 4
        assert job.failed_files == 0
        assert job.started_at is not None
        assert job.completed_at is not None

    def test_indexing_excludes_node_modules(self, repository, sample_repo_dir):
        """Test that node_modules files are excluded."""
        index_repository_task(str(repository.id), sample_repo_dir)

        files = RepositoryFile.objects.filter(repository=repository)
        paths = [f.file_path for f in files]
        assert not any("node_modules" in p for p in paths)

    def test_indexing_excludes_git(self, repository, sample_repo_dir):
        """Test that .git files are excluded."""
        index_repository_task(str(repository.id), sample_repo_dir)

        files = RepositoryFile.objects.filter(repository=repository)
        paths = [f.file_path for f in files]
        assert not any(".git" in p for p in paths)

    def test_reindexing_clears_old_data(self, repository, sample_repo_dir):
        """Test that re-indexing removes old data first."""
        # Index once
        index_repository_task(str(repository.id), sample_repo_dir)
        first_count = CodeChunk.objects.filter(repository=repository).count()

        # Index again
        index_repository_task(str(repository.id), sample_repo_dir)
        second_count = CodeChunk.objects.filter(repository=repository).count()

        # Should be the same count (not doubled)
        assert first_count == second_count

    def test_indexing_with_invalid_path(self, repository):
        """Test that indexing handles invalid path gracefully."""
        index_repository_task(str(repository.id), "/nonexistent/path")

        repository.refresh_from_db()
        assert repository.status == RepositoryStatus.ERROR

        job = IndexingJob.objects.filter(repository=repository).first()
        assert job.status == IndexingStatus.FAILED
        assert job.error_message is not None

    def test_chunk_metadata_includes_file_info(self, repository, sample_repo_dir):
        """Test that chunks have proper metadata."""
        index_repository_task(str(repository.id), sample_repo_dir)

        chunk = CodeChunk.objects.filter(
            repository=repository,
            chunk_type="function",
        ).first()

        assert chunk is not None
        assert "file_path" in chunk.metadata
        assert "language" in chunk.metadata
