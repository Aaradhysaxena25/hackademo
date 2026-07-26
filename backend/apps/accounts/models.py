"""
User models for CodePilot.
"""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.enums import SubscriptionPlan


class User(AbstractUser):
    """Custom user model for CodePilot."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(unique=True)
    github_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    github_username = models.CharField(max_length=255, blank=True, null=True)
    github_access_token = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    subscription_plan = models.CharField(
        max_length=20,
        choices=SubscriptionPlan.choices,
        default=SubscriptionPlan.FREE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "accounts_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.email
