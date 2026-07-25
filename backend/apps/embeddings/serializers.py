"""
Serializers for the embeddings app.
"""

from rest_framework import serializers


class SearchRequestSerializer(serializers.Serializer):
    """Serializer for search requests."""

    query = serializers.CharField(max_length=1000)
    repository_ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        max_length=10,
    )
    filters = serializers.DictField(required=False, default=dict)
    limit = serializers.IntegerField(required=False, default=10, min_value=1, max_value=50)


class SearchResultSerializer(serializers.Serializer):
    """Serializer for search results."""

    chunk_id = serializers.CharField()
    content = serializers.CharField()
    file_path = serializers.CharField()
    symbol_name = serializers.CharField(allow_null=True)
    chunk_type = serializers.CharField()
    start_line = serializers.IntegerField()
    end_line = serializers.IntegerField()
    language = serializers.CharField()
    relevance_score = serializers.FloatField()
    repository_id = serializers.CharField()
