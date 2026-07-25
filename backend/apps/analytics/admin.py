"""Admin configuration for analytics app."""

from django.contrib import admin

from .models import DailyUsageStats, UserActivity


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin for the UserActivity model."""

    list_display = ("user", "action", "resource_type", "created_at")
    list_filter = ("action", "resource_type")
    search_fields = ("user__email", "action")
    ordering = ("-created_at",)


@admin.register(DailyUsageStats)
class DailyUsageStatsAdmin(admin.ModelAdmin):
    """Admin for the DailyUsageStats model."""

    list_display = ("user", "date", "queries_count", "tokens_used")
    list_filter = ("date",)
    search_fields = ("user__email",)
    ordering = ("-date",)
