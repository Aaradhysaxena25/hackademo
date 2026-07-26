"""URL patterns for the repositories app."""

from django.urls import path

from . import views

app_name = "repositories"

urlpatterns = [
    path("", views.RepositoryListView.as_view(), name="list"),
    path("upload/", views.RepositoryUploadView.as_view(), name="upload"),
    path("<uuid:pk>/", views.RepositoryDetailView.as_view(), name="detail"),
    path("<uuid:pk>/reindex/", views.RepositoryReindexView.as_view(), name="reindex"),
    path("<uuid:pk>/files/", views.RepositoryFilesView.as_view(), name="files"),
]
