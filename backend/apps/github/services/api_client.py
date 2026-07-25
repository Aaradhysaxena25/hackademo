"""
GitHub API client.

Provides methods to interact with the GitHub REST API:
list repos, clone repos, fetch PRs.
"""

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"


class GitHubAPIClient:
    """
    Client for GitHub REST API v3.

    Handles authentication, pagination, and rate limiting.
    """

    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json",
        })

    def list_repositories(self, page: int = 1, per_page: int = 30) -> list[dict]:
        """
        List repositories for the authenticated user.

        Returns:
            List of repository dicts with key fields
        """
        response = self._get(
            "/user/repos",
            params={
                "page": page,
                "per_page": per_page,
                "sort": "updated",
                "direction": "desc",
                "type": "owner",
            },
        )

        if response is None:
            return []

        return [
            {
                "id": repo["id"],
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo.get("description", ""),
                "language": repo.get("language", ""),
                "private": repo["private"],
                "default_branch": repo.get("default_branch", "main"),
                "html_url": repo["html_url"],
                "clone_url": repo["clone_url"],
                "size": repo.get("size", 0),
                "updated_at": repo["updated_at"],
            }
            for repo in response
        ]

    def get_repository(self, owner: str, repo: str) -> dict | None:
        """Get a single repository's details."""
        return self._get(f"/repos/{owner}/{repo}")

    def list_branches(self, owner: str, repo: str) -> list[dict]:
        """List branches for a repository."""
        response = self._get(f"/repos/{owner}/{repo}/branches")
        if response is None:
            return []
        return [{"name": b["name"], "sha": b["commit"]["sha"]} for b in response]

    def get_pull_request(self, owner: str, repo: str, pr_number: int) -> dict | None:
        """Get a pull request with its diff."""
        return self._get(f"/repos/{owner}/{repo}/pulls/{pr_number}")

    def get_pr_files(self, owner: str, repo: str, pr_number: int) -> list[dict]:
        """Get files changed in a pull request."""
        response = self._get(f"/repos/{owner}/{repo}/pulls/{pr_number}/files")
        if response is None:
            return []
        return [
            {
                "filename": f["filename"],
                "status": f["status"],
                "additions": f["additions"],
                "deletions": f["deletions"],
                "patch": f.get("patch", ""),
            }
            for f in response
        ]

    def get_rate_limit(self) -> dict:
        """Check current rate limit status."""
        response = self._get("/rate_limit")
        if response:
            return response.get("rate", {})
        return {}

    def _get(self, endpoint: str, params: dict | None = None) -> Any:
        """Make a GET request to the GitHub API."""
        url = f"{GITHUB_API_BASE}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=15)

            if response.status_code == 403:
                # Rate limit or forbidden
                remaining = response.headers.get("X-RateLimit-Remaining", "?")
                logger.warning(f"GitHub API 403: rate limit remaining={remaining}")
                return None

            if response.status_code == 404:
                return None

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error(f"GitHub API request failed: {endpoint} - {e}")
            return None
