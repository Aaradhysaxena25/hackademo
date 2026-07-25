"""
GitHub OAuth service.

Handles the OAuth flow: generate auth URL, exchange code for token, fetch user info.
"""

import logging
from urllib.parse import urlencode

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


class GitHubOAuthService:
    """Handles GitHub OAuth authentication flow."""

    def __init__(self):
        self.client_id = settings.GITHUB_CLIENT_ID
        self.client_secret = settings.GITHUB_CLIENT_SECRET

    def get_authorization_url(self, state: str = "") -> str:
        """
        Generate the GitHub OAuth authorization URL.

        Args:
            state: CSRF protection state parameter

        Returns:
            Full authorization URL to redirect the user to
        """
        params = {
            "client_id": self.client_id,
            "scope": "repo read:user user:email",
            "state": state,
        }
        return f"{GITHUB_AUTH_URL}?{urlencode(params)}"

    def exchange_code_for_token(self, code: str) -> str | None:
        """
        Exchange the OAuth authorization code for an access token.

        Args:
            code: Authorization code from GitHub callback

        Returns:
            Access token string, or None on failure
        """
        try:
            response = requests.post(
                GITHUB_TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                },
                headers={"Accept": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                logger.error(f"GitHub OAuth error: {data['error_description']}")
                return None

            return data.get("access_token")
        except requests.RequestException as e:
            logger.error(f"GitHub OAuth token exchange failed: {e}")
            return None

    def get_user_info(self, access_token: str) -> dict | None:
        """
        Fetch the authenticated user's GitHub profile.

        Args:
            access_token: GitHub access token

        Returns:
            Dict with user info (id, login, name, email, avatar_url)
        """
        try:
            response = requests.get(
                GITHUB_USER_URL,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/vnd.github.v3+json",
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            return {
                "id": str(data["id"]),
                "login": data["login"],
                "name": data.get("name", ""),
                "email": data.get("email", ""),
                "avatar_url": data.get("avatar_url", ""),
            }
        except requests.RequestException as e:
            logger.error(f"Failed to fetch GitHub user info: {e}")
            return None
