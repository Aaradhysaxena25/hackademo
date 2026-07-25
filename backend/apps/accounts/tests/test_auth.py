"""
Tests for authentication endpoints.
"""

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "StrongPass123!",
        "first_name": "John",
        "last_name": "Doe",
    }


@pytest.fixture
def create_user(user_data):
    """Create and return a test user."""
    user = User.objects.create_user(
        username=user_data["email"],
        email=user_data["email"],
        password=user_data["password"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
    )
    return user


@pytest.mark.django_db
class TestRegister:
    """Tests for POST /api/v1/accounts/auth/register/"""

    url = "/api/v1/accounts/auth/register/"

    def test_register_success(self, api_client, user_data):
        response = api_client.post(self.url, user_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["status"] == "success"
        assert data["data"]["user"]["email"] == user_data["email"]
        assert "access" in data["data"]
        assert "refresh" in data["data"]
        assert User.objects.filter(email=user_data["email"]).exists()

    def test_register_duplicate_email(self, api_client, user_data, create_user):
        response = api_client.post(self.url, user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_weak_password(self, api_client, user_data):
        user_data["password"] = "123"
        response = api_client.post(self.url, user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_missing_fields(self, api_client):
        response = api_client.post(self.url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_invalid_email(self, api_client, user_data):
        user_data["email"] = "not-an-email"
        response = api_client.post(self.url, user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    """Tests for POST /api/v1/accounts/auth/login/"""

    url = "/api/v1/accounts/auth/login/"

    def test_login_success(self, api_client, user_data, create_user):
        response = api_client.post(
            self.url,
            {"email": user_data["email"], "password": user_data["password"]},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert "access" in data["data"]
        assert "refresh" in data["data"]
        assert data["data"]["user"]["email"] == user_data["email"]

    def test_login_wrong_password(self, api_client, user_data, create_user):
        response = api_client.post(
            self.url,
            {"email": user_data["email"], "password": "wrongpassword"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_email(self, api_client):
        response = api_client.post(
            self.url,
            {"email": "nobody@example.com", "password": "whatever"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_inactive_user(self, api_client, user_data, create_user):
        create_user.is_active = False
        create_user.save()
        response = api_client.post(
            self.url,
            {"email": user_data["email"], "password": user_data["password"]},
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestLogout:
    """Tests for POST /api/v1/accounts/auth/logout/"""

    url = "/api/v1/accounts/auth/logout/"

    def test_logout_success(self, api_client, user_data, create_user):
        # Login first
        login_response = api_client.post(
            "/api/v1/accounts/auth/login/",
            {"email": user_data["email"], "password": user_data["password"]},
            format="json",
        )
        tokens = login_response.json()["data"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

        # Logout
        response = api_client.post(
            self.url, {"refresh": tokens["refresh"]}, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

    def test_logout_unauthenticated(self, api_client):
        response = api_client.post(self.url, {"refresh": "fake"}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestProfile:
    """Tests for GET/PATCH /api/v1/accounts/profile/"""

    url = "/api/v1/accounts/profile/"

    def test_get_profile(self, api_client, create_user):
        api_client.force_authenticate(user=create_user)
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["email"] == create_user.email

    def test_get_profile_unauthenticated(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_profile(self, api_client, create_user):
        api_client.force_authenticate(user=create_user)
        response = api_client.patch(
            self.url,
            {"first_name": "Jane", "last_name": "Smith"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        create_user.refresh_from_db()
        assert create_user.first_name == "Jane"
        assert create_user.last_name == "Smith"


@pytest.mark.django_db
class TestChangePassword:
    """Tests for POST /api/v1/accounts/auth/password/change/"""

    url = "/api/v1/accounts/auth/password/change/"

    def test_change_password_success(self, api_client, user_data, create_user):
        api_client.force_authenticate(user=create_user)
        response = api_client.post(
            self.url,
            {"old_password": user_data["password"], "new_password": "NewStrong456!"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        create_user.refresh_from_db()
        assert create_user.check_password("NewStrong456!")

    def test_change_password_wrong_old(self, api_client, create_user):
        api_client.force_authenticate(user=create_user)
        response = api_client.post(
            self.url,
            {"old_password": "wrongold", "new_password": "NewStrong456!"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_change_password_weak_new(self, api_client, user_data, create_user):
        api_client.force_authenticate(user=create_user)
        response = api_client.post(
            self.url,
            {"old_password": user_data["password"], "new_password": "123"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
