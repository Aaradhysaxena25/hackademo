"""URL patterns for the embeddings app."""

from django.urls import path

from . import views

app_name = "embeddings"

urlpatterns = [
    path("search/", views.SemanticSearchView.as_view(), name="search"),
]
