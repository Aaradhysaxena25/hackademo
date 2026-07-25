"""
Serializers for the chat app.
"""

from rest_framework import serializers

from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages."""

    sources = serializers.JSONField(source="context_chunks", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "role",
            "content",
            "sources",
            "token_count",
            "model_used",
            "created_at",
        ]
        read_only_fields = fields


class ConversationListSerializer(serializers.ModelSerializer):
    """Serializer for conversation list."""

    repository_name = serializers.CharField(
        source="repository.name", read_only=True, default=None
    )
    message_count = serializers.SerializerMethodField()
    last_message_at = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "title",
            "repository_id",
            "repository_name",
            "message_count",
            "is_archived",
            "last_message_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message_at(self, obj):
        last = obj.messages.order_by("-created_at").first()
        return last.created_at if last else obj.created_at


class ConversationDetailSerializer(serializers.ModelSerializer):
    """Serializer for conversation detail with messages."""

    messages = MessageSerializer(many=True, read_only=True)
    repository_name = serializers.CharField(
        source="repository.name", read_only=True, default=None
    )

    class Meta:
        model = Conversation
        fields = [
            "id",
            "title",
            "repository_id",
            "repository_name",
            "is_archived",
            "messages",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class ConversationCreateSerializer(serializers.Serializer):
    """Serializer for creating a conversation."""

    repository_id = serializers.UUIDField()
    title = serializers.CharField(max_length=255, required=False, default="")


class SendMessageSerializer(serializers.Serializer):
    """Serializer for sending a message."""

    content = serializers.CharField(max_length=10000)
    stream = serializers.BooleanField(required=False, default=False)

    def validate_content(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Message cannot be empty.")
        return value
