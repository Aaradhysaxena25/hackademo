"""URL patterns for the analytics app."""

from django.urls import path

from . import views

app_name = "analytics"

urlpatterns = [
    path("dashboard/", views.DashboardStatsView.as_view(), name="dashboard"),
    path("repositories/<uuid:pk>/", views.RepositoryAnalyticsView.as_view(), name="repository"),
    path("usage/", views.UsageStatsView.as_view(), name="usage"),
    path("activity/", views.ActivityLogView.as_view(), name="activity"),
]
