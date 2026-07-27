"""
Tests for the analytics app.
"""

from datetime import date

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from apps.analytics.models import DailyUsageStats, UserActivity
from apps.analytics.services import ActivityTracker, AnalyticsService
from apps.chat.models import Conversation
from apps.repositories.models import Repository

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="test@example.com", email="test@example.com", password="TestPass123!"
    )


@pytest.fixture
def repository(user):
    return Repository.objects.create(
        owner=user, name="test-repo", source_type="upload", status="ready",
        total_files=100, total_chunks=500, total_size_bytes=50000,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
class TestAnalyticsService:
    def test_dashboard_stats(self, user, repository):
        Conversation.objects.create(user=user, repository=repository)
        service = AnalyticsService()
        stats = service.get_user_dashboard_stats(user)
        assert stats["total_repositories"] == 1
        assert stats["ready_repositories"] == 1
        assert stats["total_conversations"] == 1
        assert stats["total_files_indexed"] == 100

    def test_repository_analytics(self, repository):
        service = AnalyticsService()
        analytics = service.get_repository_analytics(repository)
        assert analytics["name"] == "test-repo"
        assert analytics["total_files"] == 100
        assert analytics["total_chunks"] == 0  # no actual chunks created

    def test_usage_stats_empty(self, user):
        service = AnalyticsService()
        stats = service.get_usage_stats(user, days=7)
        assert stats["period_days"] == 7
        assert stats["totals"]["queries"] == 0


@pytest.mark.django_db
class TestActivityTracker:
    def test_track_activity(self, user):
        ActivityTracker.track(user, "search", resource_type="repository", metadata={"query": "test"})
        assert UserActivity.objects.filter(user=user, action="search").count() == 1

    def test_increment_daily_stat(self, user):
        ActivityTracker.increment_daily_stat(user, "queries_count", 5)
        stat = DailyUsageStats.objects.get(user=user, date=date.today())
        assert stat.queries_count == 5

        ActivityTracker.increment_daily_stat(user, "queries_count", 3)
        stat.refresh_from_db()
        assert stat.queries_count == 8


@pytest.mark.django_db
class TestAnalyticsAPI:
    def test_dashboard_stats(self, authenticated_client, repository):
        response = authenticated_client.get("/api/v1/analytics/dashboard/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["total_repositories"] == 1

    def test_repository_analytics(self, authenticated_client, repository):
        response = authenticated_client.get(f"/api/v1/analytics/repositories/{repository.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["name"] == "test-repo"

    def test_usage_stats(self, authenticated_client):
        response = authenticated_client.get("/api/v1/analytics/usage/?days=7")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"]["period_days"] == 7

    def test_activity_log(self, authenticated_client, user):
        UserActivity.objects.create(user=user, action="login")
        response = authenticated_client.get("/api/v1/analytics/activity/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["data"]) == 1

    def test_unauthenticated(self, api_client):
        response = api_client.get("/api/v1/analytics/dashboard/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
