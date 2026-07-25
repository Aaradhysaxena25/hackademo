"""URL patterns for the analytics app."""

from django.urls import path

from . import views

app_name = "analytics"

urlpatterns = [
    path("usage/", views.UsageStatsView.as_view(), name="usage"),
    path("activity/", views.ActivityLogView.as_view(), name="activity"),
]
