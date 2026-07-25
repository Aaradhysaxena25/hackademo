"""
Common utility functions for CodePilot.
"""

import hashlib
from typing import Any

from cryptography.fernet import Fernet
from django.conf import settings


def get_fernet_key() -> bytes:
    """Get the Fernet encryption key from settings."""
    key = settings.ENCRYPTION_KEY
    if not key:
        raise ValueError("ENCRYPTION_KEY is not set in settings.")
    return key.encode() if isinstance(key, str) else key


def encrypt_value(value: str) -> str:
    """Encrypt a string value using Fernet symmetric encryption."""
    fernet = Fernet(get_fernet_key())
    return fernet.encrypt(value.encode()).decode()


def decrypt_value(encrypted_value: str) -> str:
    """Decrypt a Fernet-encrypted string value."""
    fernet = Fernet(get_fernet_key())
    return fernet.decrypt(encrypted_value.encode()).decode()


def generate_content_hash(content: str) -> str:
    """Generate a SHA-256 hash for content deduplication."""
    return hashlib.sha256(content.encode()).hexdigest()


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to a maximum length, adding ellipsis if truncated."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def chunk_list(lst: list[Any], chunk_size: int) -> list[list[Any]]:
    """Split a list into chunks of a specified size."""
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]
