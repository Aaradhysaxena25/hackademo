"""
Views for the GitHub app.

Handles OAuth flow, repository listing, and webhooks.
"""

import logging
import secrets

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.repositories.models import Repository

from .services.api_client import GitHubAPIClient
from .services.oauth import GitHubOAuthService

logger = logging.getLogger(__name__)
User = get_user_model()


class GitHubOAuthInitView(APIView):
    """
    GET /api/v1/github/oauth/

    Returns the GitHub OAuth authorization URL.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        oauth_service = GitHubOAuthService()
        state = secrets.token_urlsafe(32)

        # Store state in session or cache for CSRF verification
        # For now, include it in the URL
        auth_url = oauth_service.get_authorization_url(state=state)

        return Response(
            {
                "status": "success",
                "data": {"authorization_url": auth_url, "state": state},
            }
        )


class GitHubOAuthCallbackView(APIView):
    """
    POST /api/v1/github/callback/

    Exchange the OAuth code for a token and connect the GitHub account.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return Response(
                {"status": "error", "message": "Authorization code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        oauth_service = GitHubOAuthService()

        # Exchange code for token
        access_token = oauth_service.exchange_code_for_token(code)
        if not access_token:
            return Response(
                {"status": "error", "message": "Failed to authenticate with GitHub."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get user info
        user_info = oauth_service.get_user_info(access_token)
        if not user_info:
            return Response(
                {"status": "error", "message": "Failed to fetch GitHub profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update user with GitHub info
        user = request.user
        user.github_id = user_info["id"]
        user.github_username = user_info["login"]
        user.github_access_token = access_token  # TODO: encrypt this
        user.avatar_url = user_info["avatar_url"]
        user.save(update_fields=[
            "github_id", "github_username", "github_access_token", "avatar_url", "updated_at"
        ])

        return Response(
            {
                "status": "success",
                "data": {
                    "github_username": user_info["login"],
                    "connected": True,
                },
                "message": "GitHub account connected successfully.",
            }
        )


class GitHubDisconnectView(APIView):
    """
    POST /api/v1/github/disconnect/

    Disconnect GitHub account.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.github_id = None
        user.github_username = None
        user.github_access_token = None
        user.save(update_fields=[
            "github_id", "github_username", "github_access_token", "updated_at"
        ])

        return Response(
            {"status": "success", "message": "GitHub account disconnected."}
        )


class GitHubReposView(APIView):
    """
    GET /api/v1/github/repos/

    List the authenticated user's GitHub repositories.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.github_access_token:
            return Response(
                {"status": "error", "message": "GitHub account not connected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        page = int(request.query_params.get("page", 1))
        per_page = int(request.query_params.get("per_page", 30))

        client = GitHubAPIClient(user.github_access_token)
        repos = client.list_repositories(page=page, per_page=per_page)

        # Mark which repos are already imported
        imported_github_ids = set(
            Repository.objects.filter(owner=user, github_id__isnull=False)
            .values_list("github_id", flat=True)
        )

        for repo in repos:
            repo["already_imported"] = repo["id"] in imported_github_ids

        return Response(
            {"status": "success", "data": {"repositories": repos}}
        )


class GitHubImportView(APIView):
    """
    POST /api/v1/github/import/

    Import a repository from GitHub.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if not user.github_access_token:
            return Response(
                {"status": "error", "message": "GitHub account not connected."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        github_url = request.data.get("github_url")
        repo_name = request.data.get("name")
        branch = request.data.get("branch", "main")

        if not github_url:
            return Response(
                {"status": "error", "message": "GitHub URL is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parse owner/repo from URL
        parts = github_url.rstrip("/").split("/")
        if len(parts) < 2:
            return Response(
                {"status": "error", "message": "Invalid GitHub URL."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        owner_name, repo_slug = parts[-2], parts[-1]

        # Verify repo exists and user has access
        client = GitHubAPIClient(user.github_access_token)
        github_repo = client.get_repository(owner_name, repo_slug)

        if not github_repo:
            return Response(
                {"status": "error", "message": "Repository not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if already imported
        if Repository.objects.filter(owner=user, github_id=github_repo["id"]).exists():
            return Response(
                {"status": "error", "message": "Repository already imported."},
                status=status.HTTP_409_CONFLICT,
            )

        # Create repository record
        repository = Repository.objects.create(
            owner=user,
            name=repo_name or github_repo["name"],
            description=github_repo.get("description", "") or "",
            source_type="github",
            github_url=github_url,
            github_id=github_repo["id"],
            default_branch=branch,
            status="pending",
        )

        # TODO: Dispatch clone + index task
        # from apps.indexing.tasks import clone_and_index_task
        # clone_and_index_task.delay(str(repository.id))

        return Response(
            {
                "status": "success",
                "data": {
                    "id": str(repository.id),
                    "name": repository.name,
                    "status": repository.status,
                },
                "message": "Repository import started.",
            },
            status=status.HTTP_201_CREATED,
        )


class GitHubWebhookView(APIView):
    """
    POST /api/v1/github/webhook/

    Handle incoming GitHub webhook events (push, PR).
    """

    permission_classes = [AllowAny]

    def post(self, request):
        event_type = request.headers.get("X-GitHub-Event", "")
        # TODO: Verify webhook signature

        if event_type == "push":
            # Trigger re-index for the affected repository
            logger.info("Received push webhook event")
        elif event_type == "pull_request":
            logger.info("Received pull_request webhook event")

        return Response({"status": "success", "message": "Webhook received."})
