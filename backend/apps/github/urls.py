"""URL patterns for the GitHub app."""

from django.urls import path

from . import views

app_name = "github"

urlpatterns = [
    path("oauth/", views.GitHubOAuthInitView.as_view(), name="oauth_init"),
    path("callback/", views.GitHubOAuthCallbackView.as_view(), name="oauth_callback"),
    path("disconnect/", views.GitHubDisconnectView.as_view(), name="disconnect"),
    path("repos/", views.GitHubReposView.as_view(), name="repos"),
    path("import/", views.GitHubImportView.as_view(), name="import"),
    path("webhook/", views.GitHubWebhookView.as_view(), name="webhook"),
]
