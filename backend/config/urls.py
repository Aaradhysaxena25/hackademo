"""
URL configuration for CodePilot project.
"""

from django.contrib import admin
from django.urls import include, path

from apps.common.views import HealthCheckView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", HealthCheckView.as_view(), name="health_check"),
    path("api/v1/accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("api/v1/repositories/", include("apps.repositories.urls", namespace="repositories")),
    path("api/v1/indexing/", include("apps.indexing.urls", namespace="indexing")),
    path("api/v1/embeddings/", include("apps.embeddings.urls", namespace="embeddings")),
    path("api/v1/chat/", include("apps.chat.urls", namespace="chat")),
    path("api/v1/ai/", include("apps.ai.urls", namespace="ai")),
    path("api/v1/github/", include("apps.github.urls", namespace="github")),
    path("api/v1/analytics/", include("apps.analytics.urls", namespace="analytics")),
    path("api/v1/notifications/", include("apps.notifications.urls", namespace="notifications")),
]
