"""
Chat models for CodePilot.
"""

from django.conf import settings
from django.db import models

from apps.common.models import BaseModel
from apps.core.enums import ChatMessageRole


class Conversation(BaseModel):
    """Represents a chat conversation."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    repository = models.ForeignKey(
        "repositories.Repository",
        on_delete=models.CASCADE,
        related_name="conversations",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255, blank=True, default="New Conversation")
    is_archived = models.BooleanField(default=False)

    class Meta:
        db_table = "chat_conversation"
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.title} ({self.user.email})"


class Message(BaseModel):
    """Represents a single message in a conversation."""

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(
        max_length=20,
        choices=ChatMessageRole.choices,
    )
    content = models.TextField()
    context_chunks = models.JSONField(default=list, blank=True)
    token_count = models.IntegerField(default=0)
    model_used = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "chat_message"
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
