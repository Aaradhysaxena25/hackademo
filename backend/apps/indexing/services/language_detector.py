"""
Language detection service for source code files.
"""

import os

from .constants import LANGUAGE_EXTENSIONS


def detect_language(file_path: str) -> str:
    """
    Detect programming language from file extension.

    Args:
        file_path: Path to the file

    Returns:
        Language identifier string, or 'other' if unknown
    """
    _, ext = os.path.splitext(file_path.lower())

    # Direct extension mapping
    if ext in LANGUAGE_EXTENSIONS:
        return LANGUAGE_EXTENSIONS[ext]

    # Special file names
    basename = os.path.basename(file_path).lower()
    special_files = {
        "dockerfile": "dockerfile",
        "makefile": "makefile",
        "cmakelists.txt": "cmake",
        "rakefile": "ruby",
        "gemfile": "ruby",
        "vagrantfile": "ruby",
        "jenkinsfile": "groovy",
        ".env": "dotenv",
        ".env.example": "dotenv",
        "requirements.txt": "pip",
        "setup.py": "python",
        "setup.cfg": "ini",
        "pyproject.toml": "toml",
        "tsconfig.json": "json",
        "package.json": "json",
    }

    if basename in special_files:
        return special_files[basename]

    return "other"
