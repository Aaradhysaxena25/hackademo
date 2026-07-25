"""URL patterns for the indexing app."""

from django.urls import path

from . import views

app_name = "indexing"

urlpatterns = [
    path("jobs/<uuid:pk>/", views.IndexingJobDetailView.as_view(), name="job_detail"),
    path(
        "repositories/<uuid:repo_id>/jobs/",
        views.RepositoryIndexingJobsView.as_view(),
        name="repository_jobs",
    ),
]
