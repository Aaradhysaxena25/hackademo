"""
Repository parser service.

Walks a repository directory, applies filters, and builds a file manifest.
"""

import hashlib
import os
from dataclasses import dataclass

from .constants import MAX_FILES_PER_REPO
from .file_filter import FileFilter
from .language_detector import detect_language


@dataclass
class FileManifestEntry:
    """Represents a file discovered during repository parsing."""

    path: str  # Relative path within the repo
    name: str  # File name only
    language: str  # Detected language
    size_bytes: int  # File size
    content_hash: str  # SHA-256 hash of content
    line_count: int  # Number of lines


class RepositoryParser:
    """
    Parses a repository directory and builds a file manifest.

    Applies filtering rules to exclude binaries, node_modules,
    build artifacts, and other non-source files.
    """

    def __init__(self):
        self.file_filter = FileFilter()

    def parse(self, repo_path: str) -> list[FileManifestEntry]:
        """
        Walk the repository directory and build a manifest of indexable files.

        Args:
            repo_path: Absolute path to the repository root

        Returns:
            List of FileManifestEntry objects for files to be indexed

        Raises:
            ValueError: If the path doesn't exist or exceeds file limit
        """
        if not os.path.isdir(repo_path):
            raise ValueError(f"Repository path does not exist: {repo_path}")

        manifest = []

        for root, dirs, files in os.walk(repo_path):
            # Filter directories in-place (modifies os.walk traversal)
            dirs[:] = [
                d for d in dirs if not self.file_filter.should_skip_directory(d)
            ]

            for filename in files:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, repo_path)

                # Normalize path separators
                relative_path = relative_path.replace("\\", "/")

                try:
                    file_size = os.path.getsize(file_path)
                except OSError:
                    continue

                # Apply file filters
                if self.file_filter.should_skip_file(file_path, file_size):
                    continue

                # Check for binary
                if self.file_filter.is_binary_file(file_path):
                    continue

                # Detect language
                language = detect_language(relative_path)

                # Compute content hash and line count
                content_hash, line_count = self._compute_file_info(file_path)

                manifest.append(
                    FileManifestEntry(
                        path=relative_path,
                        name=filename,
                        language=language,
                        size_bytes=file_size,
                        content_hash=content_hash,
                        line_count=line_count,
                    )
                )

                # Safety limit
                if len(manifest) >= MAX_FILES_PER_REPO:
                    break

            if len(manifest) >= MAX_FILES_PER_REPO:
                break

        return manifest

    def _compute_file_info(self, file_path: str) -> tuple[str, int]:
        """
        Compute SHA-256 hash and line count for a file.

        Returns:
            Tuple of (content_hash, line_count)
        """
        sha256 = hashlib.sha256()
        line_count = 0

        try:
            with open(file_path, "rb") as f:
                for line in f:
                    sha256.update(line)
                    line_count += 1
        except (IOError, OSError):
            return "", 0

        return sha256.hexdigest(), line_count
