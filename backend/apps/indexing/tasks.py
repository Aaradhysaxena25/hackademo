"""
Celery tasks for the indexing pipeline.

Orchestrates: parse repo → chunk files → store chunks → update status
"""

import logging
import os
import tempfile
import zipfile

from celery import shared_task
from django.utils import timezone

from apps.core.enums import IndexingStatus, RepositoryStatus
from apps.embeddings.models import CodeChunk
from apps.indexing.models import IndexedFile, IndexingJob
from apps.repositories.models import Repository, RepositoryFile

from .services.chunker import chunk_file
from .services.parser import RepositoryParser

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
)
def index_repository_task(self, repository_id: str, repo_path: str | None = None):
    """
    Main repository indexing task.

    Parses the repository, chunks all source files, and stores
    the chunks for later embedding generation.

    Args:
        repository_id: UUID of the repository to index
        repo_path: Path to the extracted repository files (if already available)
    """
    try:
        repository = Repository.objects.get(id=repository_id)
    except Repository.DoesNotExist:
        logger.error(f"Repository {repository_id} not found")
        return

    # Create indexing job
    job = IndexingJob.objects.create(
        repository=repository,
        status=IndexingStatus.PROCESSING,
        started_at=timezone.now(),
    )

    # Update repository status
    repository.status = RepositoryStatus.INDEXING
    repository.save(update_fields=["status", "updated_at"])

    try:
        # Determine repo path
        if not repo_path:
            # For uploaded repos, use the stored path
            repo_path = _get_repository_path(repository)

        if not repo_path or not os.path.isdir(repo_path):
            raise ValueError(f"Repository path not available: {repo_path}")

        # Step 1: Parse repository files
        parser = RepositoryParser()
        manifest = parser.parse(repo_path)
        job.total_files = len(manifest)
        job.save(update_fields=["total_files"])

        logger.info(f"Indexing {repository.name}: found {len(manifest)} files")

        # Step 2: Clear old data
        RepositoryFile.objects.filter(repository=repository).delete()
        IndexedFile.objects.filter(repository=repository).delete()
        CodeChunk.objects.filter(repository=repository).delete()

        # Step 3: Process each file
        total_chunks = 0
        total_size = 0
        language_stats = {}

        for i, file_entry in enumerate(manifest):
            try:
                # Read file content
                full_path = os.path.join(repo_path, file_entry.path)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Create RepositoryFile record
                RepositoryFile.objects.create(
                    repository=repository,
                    file_path=file_entry.path,
                    file_name=file_entry.name,
                    language=file_entry.language,
                    size_bytes=file_entry.size_bytes,
                    content_hash=file_entry.content_hash,
                    line_count=file_entry.line_count,
                )

                # Create IndexedFile record
                indexed_file = IndexedFile.objects.create(
                    repository=repository,
                    indexing_job=job,
                    file_path=file_entry.path,
                    file_name=file_entry.name,
                    file_type=file_entry.language,
                    content_hash=file_entry.content_hash,
                    size_bytes=file_entry.size_bytes,
                    line_count=file_entry.line_count,
                )

                # Chunk the file
                chunks = chunk_file(content, file_entry.language, file_entry.path)

                # Store chunks
                chunk_objects = []
                for chunk in chunks:
                    chunk_objects.append(
                        CodeChunk(
                            indexed_file=indexed_file,
                            repository=repository,
                            content=chunk.content,
                            start_line=chunk.start_line,
                            end_line=chunk.end_line,
                            chunk_type=chunk.chunk_type,
                            metadata={
                                "symbol_name": chunk.symbol_name,
                                "file_path": file_entry.path,
                                "language": file_entry.language,
                                **chunk.metadata,
                            },
                        )
                    )

                if chunk_objects:
                    CodeChunk.objects.bulk_create(chunk_objects)
                    total_chunks += len(chunk_objects)

                total_size += file_entry.size_bytes

                # Track language stats
                lang = file_entry.language
                language_stats[lang] = language_stats.get(lang, 0) + 1

                # Update progress
                job.processed_files = i + 1
                job.save(update_fields=["processed_files"])

            except Exception as e:
                logger.warning(f"Error processing {file_entry.path}: {e}")
                job.failed_files += 1
                job.save(update_fields=["failed_files"])
                continue

        # Step 4: Update repository metrics
        repository.total_files = len(manifest)
        repository.total_chunks = total_chunks
        repository.total_size_bytes = total_size
        repository.languages = language_stats
        repository.status = RepositoryStatus.READY
        repository.last_indexed_at = timezone.now()
        repository.save()

        # Step 5: Complete the job
        job.status = IndexingStatus.COMPLETED
        job.completed_at = timezone.now()
        job.save()

        logger.info(
            f"Indexing complete: {repository.name} - "
            f"{len(manifest)} files, {total_chunks} chunks"
        )

    except Exception as e:
        logger.error(f"Indexing failed for {repository.name}: {e}")
        job.status = IndexingStatus.FAILED
        job.error_message = str(e)
        job.completed_at = timezone.now()
        job.save()

        repository.status = RepositoryStatus.ERROR
        repository.save(update_fields=["status", "updated_at"])

        # Retry for transient errors (not for ValueError which is permanent)
        if self.request.retries < self.max_retries and not isinstance(e, ValueError):
            raise self.retry(exc=e)


@shared_task
def process_uploaded_zip(repository_id: str, zip_path: str):
    """
    Extract a ZIP file and trigger indexing.

    Args:
        repository_id: UUID of the repository
        zip_path: Path to the uploaded ZIP file
    """
    # Create temp directory for extraction
    extract_dir = tempfile.mkdtemp(prefix=f"codepilot_repo_{repository_id}_")

    try:
        # Extract ZIP
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)

        # Find the actual repo root (might be nested in a folder)
        contents = os.listdir(extract_dir)
        if len(contents) == 1 and os.path.isdir(os.path.join(extract_dir, contents[0])):
            repo_path = os.path.join(extract_dir, contents[0])
        else:
            repo_path = extract_dir

        # Trigger indexing
        index_repository_task.delay(repository_id, repo_path)

    except zipfile.BadZipFile:
        repository = Repository.objects.get(id=repository_id)
        repository.status = RepositoryStatus.ERROR
        repository.save(update_fields=["status", "updated_at"])
        logger.error(f"Bad ZIP file for repository {repository_id}")

    finally:
        # Clean up ZIP file
        if os.path.exists(zip_path):
            os.remove(zip_path)


def _get_repository_path(repository: Repository) -> str | None:
    """Get the file system path for a repository's source files."""
    # For now, look in a standard location
    storage_base = os.environ.get(
        "REPO_STORAGE_PATH",
        os.path.join(tempfile.gettempdir(), "codepilot_repos"),
    )
    repo_path = os.path.join(storage_base, str(repository.id))
    if os.path.isdir(repo_path):
        return repo_path
    return None
