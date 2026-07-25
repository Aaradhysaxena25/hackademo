"""Admin configuration for chat app."""

from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    """Inline admin for messages within a conversation."""

    model = Message
    extra = 0
    readonly_fields = ("role", "content", "token_count", "created_at")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin for the Conversation model."""

    list_display = ("title", "user", "repository", "is_archived", "created_at")
    list_filter = ("is_archived",)
    search_fields = ("title", "user__email")
    inlines = [MessageInline]
    ordering = ("-updated_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin for the Message model."""

    list_display = ("conversation", "role", "token_count", "created_at")
    list_filter = ("role",)
    search_fields = ("content",)
    ordering = ("-created_at",)
