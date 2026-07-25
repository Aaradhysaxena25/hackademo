"""Admin configuration for accounts app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for the User model."""

    list_display = (
        "email",
        "username",
        "github_username",
        "subscription_plan",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "is_staff", "subscription_plan")
    search_fields = ("email", "username", "github_username")
    ordering = ("-created_at",)
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "CodePilot Info",
            {
                "fields": (
                    "github_id",
                    "github_username",
                    "github_access_token",
                    "avatar_url",
                    "subscription_plan",
                )
            },
        ),
    )
