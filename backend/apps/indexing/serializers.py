"""
Serializers for the indexing app.
"""

from rest_framework import serializers

from .models import IndexingJob


class IndexingJobSerializer(serializers.ModelSerializer):
    """Serializer for indexing job status."""

    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = IndexingJob
        fields = [
            "id",
            "repository_id",
            "status",
            "total_files",
            "processed_files",
            "failed_files",
            "progress_percent",
            "error_message",
            "started_at",
            "completed_at",
            "created_at",
        ]
        read_only_fields = fields

    def get_progress_percent(self, obj):
        if obj.total_files == 0:
            return 0.0
        return round((obj.processed_files / obj.total_files) * 100, 1)
