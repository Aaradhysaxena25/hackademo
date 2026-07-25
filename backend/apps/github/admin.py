"""Admin configuration for GitHub app."""

from django.contrib import admin

from .models import GitHubSyncLog, GitHubWebhook


@admin.register(GitHubWebhook)
class GitHubWebhookAdmin(admin.ModelAdmin):
    """Admin for the GitHubWebhook model."""

    list_display = ("repository", "webhook_id", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("repository__name",)


@admin.register(GitHubSyncLog)
class GitHubSyncLogAdmin(admin.ModelAdmin):
    """Admin for the GitHubSyncLog model."""

    list_display = ("user", "action", "success", "created_at")
    list_filter = ("success", "action")
    search_fields = ("user__email",)
    ordering = ("-created_at",)
