"""
Indexing models for CodePilot.
"""

from django.db import models

from apps.common.models import BaseModel
from apps.core.enums import FileType, IndexingStatus


class IndexingJob(BaseModel):
    """Represents a repository indexing job."""

    repository = models.ForeignKey(
        "repositories.Repository",
        on_delete=models.CASCADE,
        related_name="indexing_jobs",
    )
    status = models.CharField(
        max_length=20,
        choices=IndexingStatus.choices,
        default=IndexingStatus.QUEUED,
    )
    total_files = models.IntegerField(default=0)
    processed_files = models.IntegerField(default=0)
    failed_files = models.IntegerField(default=0)
    error_message = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "indexing_job"
        verbose_name = "Indexing Job"
        verbose_name_plural = "Indexing Jobs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"IndexingJob({self.repository.name} - {self.status})"


class IndexedFile(BaseModel):
    """Represents an indexed file from a repository."""

    repository = models.ForeignKey(
        "repositories.Repository",
        on_delete=models.CASCADE,
        related_name="indexed_files",
    )
    indexing_job = models.ForeignKey(
        IndexingJob,
        on_delete=models.SET_NULL,
        null=True,
        related_name="indexed_files",
    )
    file_path = models.CharField(max_length=1024)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(
        max_length=20,
        choices=FileType.choices,
        default=FileType.OTHER,
    )
    content_hash = models.CharField(max_length=64)
    size_bytes = models.IntegerField(default=0)
    line_count = models.IntegerField(default=0)

    class Meta:
        db_table = "indexing_indexed_file"
        verbose_name = "Indexed File"
        verbose_name_plural = "Indexed Files"
        unique_together = ("repository", "file_path")
        ordering = ["file_path"]

    def __str__(self):
        return self.file_path
