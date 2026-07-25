"""
Tests for the embeddings service and semantic search.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from apps.embeddings.models import CodeChunk
from apps.embeddings.services.generator import EmbeddingGenerator
from apps.embeddings.services.search import SemanticSearchService
from apps.indexing.models import IndexedFile, IndexingJob
from apps.repositories.models import Repository

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="test@example.com",
        email="test@example.com",
        password="TestPass123!",
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        username="other@example.com",
        email="other@example.com",
        password="TestPass123!",
    )


@pytest.fixture
def repository(user):
    return Repository.objects.create(
        owner=user,
        name="test-repo",
        source_type="upload",
        status="ready",
    )


@pytest.fixture
def indexed_file(repository):
    job = IndexingJob.objects.create(repository=repository, status="completed")
    return IndexedFile.objects.create(
        repository=repository,
        indexing_job=job,
        file_path="src/auth.py",
        file_name="auth.py",
        file_type="python",
        content_hash="abc123",
        size_bytes=1000,
        line_count=50,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


class TestEmbeddingGenerator:
    """Tests for the embedding generator service."""

    def test_generate_single_embedding(self):
        generator = EmbeddingGenerator()
        embedding = generator.generate_embedding("def hello(): print('hi')")
        assert isinstance(embedding, list)
        assert len(embedding) == 384  # all-MiniLM-L6-v2 dimensions

    def test_generate_batch_embeddings(self):
        generator = EmbeddingGenerator()
        texts = [
            "function to validate email",
            "class for database connection",
            "error handling middleware",
        ]
        embeddings = generator.generate_embeddings_batch(texts)
        assert len(embeddings) == 3
        assert all(len(e) == 384 for e in embeddings)

    def test_embeddings_are_normalized(self):
        """Normalized embeddings have L2 norm of ~1.0."""
        import numpy as np

        generator = EmbeddingGenerator()
        embedding = generator.generate_embedding("test code")
        norm = np.linalg.norm(embedding)
        assert abs(norm - 1.0) < 0.01

    def test_similar_texts_have_high_similarity(self):
        generator = EmbeddingGenerator()
        emb1 = generator.generate_embedding("function to validate user email address")
        emb2 = generator.generate_embedding("method that checks if email is valid")
        similarity = generator.compute_similarity(emb1, emb2)
        assert similarity > 0.5  # Similar texts should score high

    def test_different_texts_have_low_similarity(self):
        generator = EmbeddingGenerator()
        emb1 = generator.generate_embedding("function to validate email")
        emb2 = generator.generate_embedding("recipe for chocolate cake ingredients")
        similarity = generator.compute_similarity(emb1, emb2)
        assert similarity < 0.5  # Different topics should score low

    def test_augment_text(self):
        generator = EmbeddingGenerator()
        metadata = {
            "file_path": "src/auth.py",
            "language": "python",
            "symbol_name": "validate_token",
        }
        augmented = generator.augment_text("def validate_token():", metadata)
        assert "File: src/auth.py" in augmented
        assert "Language: python" in augmented
        assert "Symbol: validate_token" in augmented

    def test_empty_batch(self):
        generator = EmbeddingGenerator()
        embeddings = generator.generate_embeddings_batch([])
        assert embeddings == []


@pytest.mark.django_db
class TestSemanticSearch:
    """Tests for the semantic search service."""

    def _create_chunks_with_embeddings(self, repository, indexed_file):
        """Helper to create chunks with real embeddings."""
        generator = EmbeddingGenerator()

        chunks_data = [
            {
                "content": "def authenticate_user(email, password):\n    user = User.objects.get(email=email)\n    return user.check_password(password)",
                "chunk_type": "function",
                "metadata": {"file_path": "src/auth.py", "language": "python", "symbol_name": "authenticate_user"},
                "start_line": 1,
                "end_line": 3,
            },
            {
                "content": "def connect_database(host, port, dbname):\n    return psycopg2.connect(host=host, port=port, dbname=dbname)",
                "chunk_type": "function",
                "metadata": {"file_path": "src/db.py", "language": "python", "symbol_name": "connect_database"},
                "start_line": 1,
                "end_line": 2,
            },
            {
                "content": "class UserSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = User\n        fields = ['id', 'email', 'name']",
                "chunk_type": "class",
                "metadata": {"file_path": "src/serializers.py", "language": "python", "symbol_name": "UserSerializer"},
                "start_line": 1,
                "end_line": 4,
            },
        ]

        chunks = []
        for data in chunks_data:
            augmented = generator.augment_text(data["content"], data["metadata"])
            embedding = generator.generate_embedding(augmented)

            chunk = CodeChunk.objects.create(
                indexed_file=indexed_file,
                repository=repository,
                content=data["content"],
                chunk_type=data["chunk_type"],
                metadata=data["metadata"],
                start_line=data["start_line"],
                end_line=data["end_line"],
                embedding=embedding,
            )
            chunks.append(chunk)

        return chunks

    def test_search_returns_relevant_results(self, repository, indexed_file):
        self._create_chunks_with_embeddings(repository, indexed_file)

        service = SemanticSearchService()
        results = service.search(
            query="how does user authentication work",
            repository_ids=[str(repository.id)],
        )

        assert len(results) > 0
        # Auth-related chunk should be most relevant
        assert "auth" in results[0].file_path or "authenticate" in results[0].content

    def test_search_respects_repository_scope(self, user, indexed_file, repository):
        self._create_chunks_with_embeddings(repository, indexed_file)

        # Create another repo with no chunks
        other_repo = Repository.objects.create(
            owner=user, name="empty-repo", source_type="upload", status="ready"
        )

        service = SemanticSearchService()
        results = service.search(
            query="authentication",
            repository_ids=[str(other_repo.id)],
        )
        assert len(results) == 0

    def test_search_limit(self, repository, indexed_file):
        self._create_chunks_with_embeddings(repository, indexed_file)

        service = SemanticSearchService()
        results = service.search(
            query="python code",
            repository_ids=[str(repository.id)],
            limit=1,
        )
        assert len(results) <= 1

    def test_search_min_score_threshold(self, repository, indexed_file):
        self._create_chunks_with_embeddings(repository, indexed_file)

        service = SemanticSearchService()
        results = service.search(
            query="chocolate cake recipe baking",  # Totally unrelated
            repository_ids=[str(repository.id)],
            min_score=0.8,  # Very high threshold
        )
        assert len(results) == 0


@pytest.mark.django_db
class TestSearchAPI:
    """Tests for the search API endpoint."""

    url = "/api/v1/embeddings/search/"

    def test_search_unauthenticated(self, api_client):
        response = api_client.post(self.url, {}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_search_missing_query(self, authenticated_client, repository):
        response = authenticated_client.post(
            self.url,
            {"repository_ids": [str(repository.id)]},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_search_missing_repos(self, authenticated_client):
        response = authenticated_client.post(
            self.url,
            {"query": "test"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_search_other_users_repo(self, api_client, other_user, repository):
        api_client.force_authenticate(user=other_user)
        response = api_client.post(
            self.url,
            {"query": "test", "repository_ids": [str(repository.id)]},
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_search_success(self, authenticated_client, repository, indexed_file):
        """Test successful search returns proper format."""
        # Create a chunk with embedding
        generator = EmbeddingGenerator()
        embedding = generator.generate_embedding("authentication login user")
        CodeChunk.objects.create(
            indexed_file=indexed_file,
            repository=repository,
            content="def login(email, password): pass",
            chunk_type="function",
            metadata={"file_path": "auth.py", "language": "python"},
            start_line=1,
            end_line=1,
            embedding=embedding,
        )

        response = authenticated_client.post(
            self.url,
            {"query": "user login", "repository_ids": [str(repository.id)]},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert "results" in data["data"]
        assert "query_time_ms" in data["data"]
