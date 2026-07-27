"""
Tests for the GitHub integration.
"""

from unittest.mock import MagicMock, patch

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from apps.github.services.oauth import GitHubOAuthService
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
def github_user(user):
    user.github_id = "12345"
    user.github_username = "testuser"
    user.github_access_token = "ghp_test_token_123"
    user.save()
    return user


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def github_authenticated_client(api_client, github_user):
    api_client.force_authenticate(user=github_user)
    return api_client


class TestGitHubOAuthService:
    """Tests for the OAuth service."""

    def test_get_authorization_url(self):
        service = GitHubOAuthService()
        url = service.get_authorization_url(state="test-state")
        assert "github.com/login/oauth/authorize" in url
        assert "state=test-state" in url
        assert "scope=repo" in url


@pytest.mark.django_db
class TestGitHubOAuthInit:
    """Tests for GET /api/v1/github/oauth/"""

    url = "/api/v1/github/oauth/"

    def test_get_auth_url(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "authorization_url" in data["data"]
        assert "github.com" in data["data"]["authorization_url"]

    def test_unauthenticated(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestGitHubCallback:
    """Tests for POST /api/v1/github/callback/"""

    url = "/api/v1/github/callback/"

    def test_missing_code(self, authenticated_client):
        response = authenticated_client.post(self.url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch("apps.github.views.GitHubOAuthService")
    def test_successful_callback(self, mock_service_class, authenticated_client, user):
        mock_service = MagicMock()
        mock_service.exchange_code_for_token.return_value = "ghp_token123"
        mock_service.get_user_info.return_value = {
            "id": "67890",
            "login": "octocat",
            "name": "Octo Cat",
            "email": "octo@github.com",
            "avatar_url": "https://github.com/octocat.png",
        }
        mock_service_class.return_value = mock_service

        response = authenticated_client.post(
            self.url, {"code": "test_auth_code"}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["github_username"] == "octocat"
        assert data["data"]["connected"] is True

        user.refresh_from_db()
        assert user.github_username == "octocat"
        assert user.github_id == "67890"

    @patch("apps.github.views.GitHubOAuthService")
    def test_failed_token_exchange(self, mock_service_class, authenticated_client):
        mock_service = MagicMock()
        mock_service.exchange_code_for_token.return_value = None
        mock_service_class.return_value = mock_service

        response = authenticated_client.post(
            self.url, {"code": "bad_code"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGitHubDisconnect:
    """Tests for POST /api/v1/github/disconnect/"""

    url = "/api/v1/github/disconnect/"

    def test_disconnect(self, github_authenticated_client, github_user):
        response = github_authenticated_client.post(self.url)
        assert response.status_code == status.HTTP_200_OK

        github_user.refresh_from_db()
        assert github_user.github_id is None
        assert github_user.github_username is None
        assert github_user.github_access_token is None


@pytest.mark.django_db
class TestGitHubRepos:
    """Tests for GET /api/v1/github/repos/"""

    url = "/api/v1/github/repos/"

    def test_not_connected(self, authenticated_client):
        response = authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch("apps.github.views.GitHubAPIClient")
    def test_list_repos(self, mock_client_class, github_authenticated_client):
        mock_client = MagicMock()
        mock_client.list_repositories.return_value = [
            {
                "id": 1,
                "name": "my-repo",
                "full_name": "user/my-repo",
                "description": "Test",
                "language": "Python",
                "private": False,
                "default_branch": "main",
                "html_url": "https://github.com/user/my-repo",
                "clone_url": "https://github.com/user/my-repo.git",
                "size": 1024,
                "updated_at": "2024-01-01T00:00:00Z",
            }
        ]
        mock_client_class.return_value = mock_client

        response = github_authenticated_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        repos = response.json()["data"]["repositories"]
        assert len(repos) == 1
        assert repos[0]["name"] == "my-repo"


@pytest.mark.django_db
class TestGitHubImport:
    """Tests for POST /api/v1/github/import/"""

    url = "/api/v1/github/import/"

    def test_not_connected(self, authenticated_client):
        response = authenticated_client.post(
            self.url, {"github_url": "https://github.com/user/repo"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_url(self, github_authenticated_client):
        response = github_authenticated_client.post(self.url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @patch("apps.github.views.GitHubAPIClient")
    def test_successful_import(self, mock_client_class, github_authenticated_client):
        mock_client = MagicMock()
        mock_client.get_repository.return_value = {
            "id": 999,
            "name": "awesome-project",
            "description": "An awesome project",
            "default_branch": "main",
        }
        mock_client_class.return_value = mock_client

        response = github_authenticated_client.post(
            self.url,
            {"github_url": "https://github.com/user/awesome-project"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["data"]["name"] == "awesome-project"
        assert Repository.objects.filter(github_id=999).exists()

    @patch("apps.github.views.GitHubAPIClient")
    def test_duplicate_import(self, mock_client_class, github_authenticated_client, github_user):
        # Create existing repo
        Repository.objects.create(
            owner=github_user, name="existing", source_type="github", github_id=999
        )

        mock_client = MagicMock()
        mock_client.get_repository.return_value = {"id": 999, "name": "existing"}
        mock_client_class.return_value = mock_client

        response = github_authenticated_client.post(
            self.url,
            {"github_url": "https://github.com/user/existing"},
            format="json",
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    @patch("apps.github.views.GitHubAPIClient")
    def test_repo_not_found(self, mock_client_class, github_authenticated_client):
        mock_client = MagicMock()
        mock_client.get_repository.return_value = None
        mock_client_class.return_value = mock_client

        response = github_authenticated_client.post(
            self.url,
            {"github_url": "https://github.com/user/nonexistent"},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
