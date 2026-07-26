"""Serializers for the analytics app."""

from rest_framework import serializers

from .models import UserActivity


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ["id", "action", "resource_type", "resource_id", "metadata", "created_at"]
        read_only_fields = fields
