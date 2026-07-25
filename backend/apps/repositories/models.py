"""
Repository models for CodePilot.
"""

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.core.enums import RepositoryStatus


class Repository(BaseModel):
    """
    Represents a code repository imported by a user.

    Supports two source types:
    - GitHub: cloned via GitHub API
    - Upload: manually uploaded as ZIP/TAR archive
    """

    class SourceType(models.TextChoices):
        GITHUB = "github", "GitHub"
        UPLOAD = "upload", "Upload"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="repositories",
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    source_type = models.CharField(
        max_length=20,
        choices=SourceType.choices,
        default=SourceType.UPLOAD,
    )

    # GitHub-specific fields
    github_url = models.URLField(blank=True, default="")
    github_id = models.BigIntegerField(blank=True, null=True)
    default_branch = models.CharField(max_length=100, default="main")

    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=RepositoryStatus.choices,
        default=RepositoryStatus.PENDING,
    )

    # Metrics (updated after indexing)
    total_files = models.IntegerField(default=0)
    total_chunks = models.IntegerField(default=0)
    total_size_bytes = models.BigIntegerField(default=0)
    languages = models.JSONField(default=dict, blank=True)

    # Timestamps
    last_indexed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "repositories_repository"
        verbose_name = "Repository"
        verbose_name_plural = "Repositories"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.owner.email}/{self.name}"


class RepositoryFile(BaseModel):
    """
    Represents an individual file within a repository.
    Created during the indexing process.
    """

    repository = models.ForeignKey(
        Repository,
        on_delete=models.CASCADE,
        related_name="files",
    )
    file_path = models.CharField(max_length=1000)
    file_name = models.CharField(max_length=255)
    language = models.CharField(max_length=50, blank=True, default="")
    size_bytes = models.BigIntegerField(default=0)
    content_hash = models.CharField(max_length=64, blank=True, default="")
    line_count = models.IntegerField(default=0)

    class Meta:
        db_table = "repositories_file"
        verbose_name = "Repository File"
        verbose_name_plural = "Repository Files"
        ordering = ["file_path"]
        unique_together = ("repository", "file_path")

    def __str__(self):
        return self.file_path
