"""
AI models for CodePilot.

Tracks AI model usage and configurations.
"""

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class AIModelConfig(BaseModel):
    """Configuration for AI models used in the system."""

    name = models.CharField(max_length=100, unique=True)
    provider = models.CharField(max_length=50)  # openai, anthropic, etc.
    model_id = models.CharField(max_length=100)  # gpt-4, claude-3, etc.
    max_tokens = models.IntegerField(default=4096)
    temperature = models.FloatField(default=0.7)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "ai_model_config"
        verbose_name = "AI Model Config"
        verbose_name_plural = "AI Model Configs"

    def __str__(self):
        return f"{self.name} ({self.provider}/{self.model_id})"


class AIUsageLog(BaseModel):
    """Tracks AI API usage for monitoring and billing."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_usage_logs",
    )
    model_config = models.ForeignKey(
        AIModelConfig,
        on_delete=models.SET_NULL,
        null=True,
        related_name="usage_logs",
    )
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    cost_usd = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    request_type = models.CharField(max_length=50)  # chat, embedding, etc.

    class Meta:
        db_table = "ai_usage_log"
        verbose_name = "AI Usage Log"
        verbose_name_plural = "AI Usage Logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.total_tokens} tokens"
