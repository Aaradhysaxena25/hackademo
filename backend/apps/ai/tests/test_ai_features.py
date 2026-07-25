"""
Tests for AI feature endpoints and services.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from apps.ai.services.features import AIFeatureService
from apps.ai.services.llm_provider import MockProvider
from apps.embeddings.models import CodeChunk
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
        owner=user, name="test-repo", source_type="upload", status="ready"
    )


@pytest.fixture
def code_chunk(repository):
    job = IndexingJob.objects.create(repository=repository, status="completed")
    indexed_file = IndexedFile.objects.create(
        repository=repository,
        indexing_job=job,
        file_path="src/auth.py",
        file_name="auth.py",
        file_type="python",
        content_hash="abc",
        size_bytes=500,
        line_count=20,
    )
    return CodeChunk.objects.create(
        indexed_file=indexed_file,
        repository=repository,
        content='def authenticate(email, password):\n    """Authenticate a user."""\n    user = User.objects.get(email=email)\n    if user.check_password(password):\n        return generate_token(user)\n    raise AuthError("Invalid credentials")',
        chunk_type="function",
        start_line=10,
        end_line=16,
        metadata={
            "file_path": "src/auth.py",
            "language": "python",
            "symbol_name": "authenticate",
            "parameters": ["email", "password"],
        },
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
class TestAIFeatureService:
    """Tests for AIFeatureService with mock LLM."""

    def test_explain_code(self, code_chunk):
        mock_llm = MockProvider(response="This function authenticates users by email and password.")
        service = AIFeatureService(llm_provider=mock_llm)
        result = service.explain_code(str(code_chunk.id))
        assert result.content == "This function authenticates users by email and password."
        assert result.feature == "explain"
        assert result.chunk_id == str(code_chunk.id)

    def test_generate_docs(self, code_chunk):
        mock_llm = MockProvider(response='"""Authenticate a user.\n\nArgs:\n    email: User email\n    password: User password"""')
        service = AIFeatureService(llm_provider=mock_llm)
        result = service.generate_docs(str(code_chunk.id))
        assert result.feature == "generate_docs"
        assert len(result.content) > 0

    def test_generate_tests(self, code_chunk):
        mock_llm = MockProvider(response="def test_authenticate_success():\n    assert authenticate('a@b.com', 'pass')")
        service = AIFeatureService(llm_provider=mock_llm)
        result = service.generate_tests(str(code_chunk.id), framework="pytest")
        assert result.feature == "generate_tests"
        assert result.metadata["framework"] == "pytest"

    def test_generate_tests_auto_framework(self, code_chunk):
        mock_llm = MockProvider(response="test code")
        service = AIFeatureService(llm_provider=mock_llm)
        result = service.generate_tests(str(code_chunk.id), framework="auto")
        assert result.metadata["framework"] == "pytest"  # Python → pytest

    def test_detect_bugs(self, code_chunk):
        mock_llm = MockProvider(response="No critical bugs found. Minor: missing input validation.")
        service = AIFeatureService(llm_provider=mock_llm)
        result = service.detect_bugs(str(code_chunk.id))
        assert result.feature == "detect_bugs"
        assert len(result.content) > 0

    def test_invalid_chunk_id(self):
        import uuid
        mock_llm = MockProvider(response="test")
        service = AIFeatureService(llm_provider=mock_llm)
        with pytest.raises(ValueError, match="Code chunk not found"):
            service.explain_code(str(uuid.uuid4()))


@pytest.mark.django_db
class TestExplainAPI:
    """Tests for POST /api/v1/ai/explain/"""

    url = "/api/v1/ai/explain/"

    def test_explain_success(self, authenticated_client, code_chunk):
        response = authenticated_client.post(
            self.url, {"chunk_id": str(code_chunk.id)}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["feature"] == "explain"

    def test_explain_not_found(self, authenticated_client):
        import uuid
        response = authenticated_client.post(
            self.url, {"chunk_id": str(uuid.uuid4())}, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_explain_not_owner(self, api_client, other_user, code_chunk):
        api_client.force_authenticate(user=other_user)
        response = api_client.post(
            self.url, {"chunk_id": str(code_chunk.id)}, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_explain_unauthenticated(self, api_client, code_chunk):
        response = api_client.post(
            self.url, {"chunk_id": str(code_chunk.id)}, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestGenerateDocsAPI:
    """Tests for POST /api/v1/ai/generate-docs/"""

    url = "/api/v1/ai/generate-docs/"

    def test_generate_docs_success(self, authenticated_client, code_chunk):
        response = authenticated_client.post(
            self.url, {"chunk_id": str(code_chunk.id)}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["feature"] == "generate_docs"

    def test_generate_docs_with_format(self, authenticated_client, code_chunk):
        response = authenticated_client.post(
            self.url,
            {"chunk_id": str(code_chunk.id), "format": "docstring"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestGenerateTestsAPI:
    """Tests for POST /api/v1/ai/generate-tests/"""

    url = "/api/v1/ai/generate-tests/"

    def test_generate_tests_success(self, authenticated_client, code_chunk):
        response = authenticated_client.post(
            self.url, {"chunk_id": str(code_chunk.id)}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["feature"] == "generate_tests"

    def test_generate_tests_with_framework(self, authenticated_client, code_chunk):
        response = authenticated_client.post(
            self.url,
            {"chunk_id": str(code_chunk.id), "framework": "jest"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestDetectBugsAPI:
    """Tests for POST /api/v1/ai/detect-bugs/"""

    url = "/api/v1/ai/detect-bugs/"

    def test_detect_bugs_success(self, authenticated_client, code_chunk):
        response = authenticated_client.post(
            self.url, {"chunk_id": str(code_chunk.id)}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["feature"] == "detect_bugs"

    def test_detect_bugs_invalid_chunk(self, authenticated_client):
        import uuid
        response = authenticated_client.post(
            self.url, {"chunk_id": str(uuid.uuid4())}, format="json"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
