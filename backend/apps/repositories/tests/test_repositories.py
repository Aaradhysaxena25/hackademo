"""
Tests for repository endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from apps.repositories.models import Repository, RepositoryFile

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser@example.com",
        email="testuser@example.com",
        password="TestPass123!",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def other_user():
    return User.objects.create_user(
        username="other@example.com",
        email="other@example.com",
        password="TestPass123!",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def repository(user):
    return Repository.objects.create(
        owner=user,
        name="test-repo",
        description="A test repository",
        source_type="upload",
        status="ready",
        total_files=10,
        total_chunks=50,
    )


@pytest.fixture
def repository_with_files(repository):
    RepositoryFile.objects.create(
        repository=repository,
        file_path="src/main.py",
        file_name="main.py",
        language="python",
        size_bytes=1024,
        line_count=50,
    )
    RepositoryFile.objects.create(
        repository=repository,
        file_path="src/utils.py",
        file_name="utils.py",
        language="python",
        size_bytes=512,
        line_count=25,
    )
    RepositoryFile.objects.create(
        repository=repository,
        file_path="README.md",
        file_name="README.md",
        language="markdown",
        size_bytes=256,
        line_count=10,
    )
    return repository


@pytest.mark.django_db
class TestRepositoryList:
    """Tests for GET /api/v1/repositories/"""

    url = "/api/v1/repositories/"

    def test_list_repositories(self, authenticated_client, repository):
        response = authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 1
        assert data["results"][0]["name"] == "test-repo"

    def test_list_repositories_unauthenticated(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_only_own_repositories(self, authenticated_client, repository, other_user):
        # Create repo for other user
        Repository.objects.create(owner=other_user, name="other-repo", source_type="upload")
        response = authenticated_client.get(self.url)
        assert response.json()["count"] == 1

    def test_filter_by_status(self, authenticated_client, user):
        Repository.objects.create(owner=user, name="pending-repo", source_type="upload", status="pending")
        Repository.objects.create(owner=user, name="ready-repo", source_type="upload", status="ready")
        response = authenticated_client.get(f"{self.url}?status=ready")
        assert response.json()["count"] == 1
        assert response.json()["results"][0]["name"] == "ready-repo"

    def test_search_by_name(self, authenticated_client, user):
        Repository.objects.create(owner=user, name="django-app", source_type="upload")
        Repository.objects.create(owner=user, name="react-app", source_type="upload")
        response = authenticated_client.get(f"{self.url}?search=django")
        assert response.json()["count"] == 1


@pytest.mark.django_db
class TestRepositoryCreate:
    """Tests for POST /api/v1/repositories/"""

    url = "/api/v1/repositories/"

    def test_create_upload_repository(self, authenticated_client):
        data = {"name": "my-project", "description": "My project", "source_type": "upload"}
        response = authenticated_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["data"]["name"] == "my-project"
        assert response.json()["data"]["status"] == "pending"

    def test_create_github_repository(self, authenticated_client):
        data = {
            "name": "github-project",
            "source_type": "github",
            "github_url": "https://github.com/user/repo",
        }
        response = authenticated_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["data"]["source_type"] == "github"

    def test_create_github_without_url(self, authenticated_client):
        data = {"name": "bad-repo", "source_type": "github"}
        response = authenticated_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_invalid_name(self, authenticated_client):
        data = {"name": "<script>alert('xss')</script>", "source_type": "upload"}
        response = authenticated_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_unauthenticated(self, api_client):
        data = {"name": "test", "source_type": "upload"}
        response = api_client.post(self.url, data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRepositoryDetail:
    """Tests for GET/PATCH/DELETE /api/v1/repositories/{id}/"""

    def test_get_detail(self, authenticated_client, repository):
        url = f"/api/v1/repositories/{repository.id}/"
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["name"] == "test-repo"

    def test_get_detail_not_owner(self, api_client, repository, other_user):
        api_client.force_authenticate(user=other_user)
        url = f"/api/v1/repositories/{repository.id}/"
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_repository(self, authenticated_client, repository):
        url = f"/api/v1/repositories/{repository.id}/"
        response = authenticated_client.patch(url, {"description": "Updated"}, format="json")
        assert response.status_code == status.HTTP_200_OK
        repository.refresh_from_db()
        assert repository.description == "Updated"

    def test_delete_repository(self, authenticated_client, repository):
        url = f"/api/v1/repositories/{repository.id}/"
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Repository.objects.filter(id=repository.id).exists()

    def test_delete_cascades_files(self, authenticated_client, repository_with_files):
        repo_id = repository_with_files.id
        url = f"/api/v1/repositories/{repo_id}/"
        authenticated_client.delete(url)
        assert RepositoryFile.objects.filter(repository_id=repo_id).count() == 0


@pytest.mark.django_db
class TestRepositoryFiles:
    """Tests for GET /api/v1/repositories/{id}/files/"""

    def test_list_files(self, authenticated_client, repository_with_files):
        url = f"/api/v1/repositories/{repository_with_files.id}/files/"
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["count"] == 3

    def test_filter_by_language(self, authenticated_client, repository_with_files):
        url = f"/api/v1/repositories/{repository_with_files.id}/files/?language=python"
        response = authenticated_client.get(url)
        assert response.json()["count"] == 2

    def test_search_files(self, authenticated_client, repository_with_files):
        url = f"/api/v1/repositories/{repository_with_files.id}/files/?search=main"
        response = authenticated_client.get(url)
        assert response.json()["count"] == 1

    def test_filter_by_path(self, authenticated_client, repository_with_files):
        url = f"/api/v1/repositories/{repository_with_files.id}/files/?path=src/"
        response = authenticated_client.get(url)
        assert response.json()["count"] == 2


@pytest.mark.django_db
class TestRepositoryReindex:
    """Tests for POST /api/v1/repositories/{id}/reindex/"""

    def test_reindex(self, authenticated_client, repository):
        url = f"/api/v1/repositories/{repository.id}/reindex/"
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_202_ACCEPTED
        repository.refresh_from_db()
        assert repository.status == "pending"

    def test_reindex_already_indexing(self, authenticated_client, repository):
        repository.status = "indexing"
        repository.save()
        url = f"/api/v1/repositories/{repository.id}/reindex/"
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_409_CONFLICT
