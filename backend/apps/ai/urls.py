"""URL patterns for the AI app."""

from django.urls import path

from . import views

app_name = "ai"

urlpatterns = [
    path("explain/", views.ExplainCodeView.as_view(), name="explain"),
    path("generate-docs/", views.GenerateDocsView.as_view(), name="generate_docs"),
    path("generate-tests/", views.GenerateTestsView.as_view(), name="generate_tests"),
    path("detect-bugs/", views.DetectBugsView.as_view(), name="detect_bugs"),
]
