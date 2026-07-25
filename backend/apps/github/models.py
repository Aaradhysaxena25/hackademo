"""
GitHub integration models for CodePilot.
"""

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class GitHubWebhook(BaseModel):
    """Tracks GitHub webhooks registered for repositories."""

    repository = models.ForeignKey(
        "repositories.Repository",
        on_delete=models.CASCADE,
        related_name="webhooks",
    )
    webhook_id = models.BigIntegerField(unique=True)
    events = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "github_webhook"
        verbose_name = "GitHub Webhook"
        verbose_name_plural = "GitHub Webhooks"

    def __str__(self):
        return f"Webhook({self.repository.name} - {self.webhook_id})"


class GitHubSyncLog(BaseModel):
    """Logs GitHub sync operations."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sync_logs",
    )
    action = models.CharField(max_length=100)
    details = models.JSONField(default=dict, blank=True)
    success = models.BooleanField(default=True)

    class Meta:
        db_table = "github_sync_log"
        verbose_name = "GitHub Sync Log"
        verbose_name_plural = "GitHub Sync Logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.action}"
