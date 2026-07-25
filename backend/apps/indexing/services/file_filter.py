"""
File filtering service for the indexing pipeline.

Determines which files should be indexed and which should be skipped.
"""

import os

from .constants import (
    EXCLUDED_DIRECTORIES,
    EXCLUDED_EXTENSIONS,
    EXCLUDED_FILES,
    MAX_FILE_SIZE,
)


class FileFilter:
    """
    Filters files during repository traversal.

    Applies exclusion rules for directories, extensions, binary files,
    and file size limits.
    """

    def should_skip_directory(self, dir_name: str) -> bool:
        """Check if a directory should be skipped."""
        return dir_name in EXCLUDED_DIRECTORIES or dir_name.startswith(".")

    def should_skip_file(self, file_path: str, file_size: int = 0) -> bool:
        """
        Check if a file should be skipped.

        Args:
            file_path: Full path to the file
            file_size: Size of the file in bytes

        Returns:
            True if the file should be skipped
        """
        basename = os.path.basename(file_path).lower()
        _, ext = os.path.splitext(file_path.lower())

        # Skip by specific file name
        if basename in EXCLUDED_FILES:
            return True

        # Skip by extension
        if ext in EXCLUDED_EXTENSIONS:
            return True

        # Skip minified files
        if basename.endswith(".min.js") or basename.endswith(".min.css"):
            return True

        # Skip by file size
        if file_size > MAX_FILE_SIZE:
            return True

        return False

    def is_binary_file(self, file_path: str) -> bool:
        """
        Detect if a file is binary by reading first 8KB and checking for null bytes.

        Args:
            file_path: Path to the file

        Returns:
            True if the file appears to be binary
        """
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(8192)

            # Check for null bytes
            if b"\x00" in chunk:
                return True

            # Try decoding as UTF-8
            try:
                chunk.decode("utf-8")
                return False
            except UnicodeDecodeError:
                return True

        except (IOError, OSError):
            return True  # Assume binary if can't read
