"""
Analytics models for CodePilot.
"""

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class UserActivity(BaseModel):
    """Tracks user activity for analytics."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
    )
    action = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=100, blank=True, null=True)
    resource_id = models.UUIDField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        db_table = "analytics_user_activity"
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.action}"


class DailyUsageStats(BaseModel):
    """Aggregated daily usage statistics."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_stats",
    )
    date = models.DateField()
    queries_count = models.IntegerField(default=0)
    tokens_used = models.IntegerField(default=0)
    repositories_indexed = models.IntegerField(default=0)

    class Meta:
        db_table = "analytics_daily_usage_stats"
        verbose_name = "Daily Usage Stats"
        verbose_name_plural = "Daily Usage Stats"
        unique_together = ("user", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.email} - {self.date}"
