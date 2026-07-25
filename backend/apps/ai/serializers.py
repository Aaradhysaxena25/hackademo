"""
Serializers for AI feature endpoints.
"""

from rest_framework import serializers


class ExplainRequestSerializer(serializers.Serializer):
    """Request to explain code."""

    chunk_id = serializers.UUIDField()
    detail_level = serializers.ChoiceField(
        choices=["brief", "detailed"], default="detailed"
    )


class GenerateDocsRequestSerializer(serializers.Serializer):
    """Request to generate documentation."""

    chunk_id = serializers.UUIDField()
    format = serializers.ChoiceField(
        choices=["markdown", "docstring"], default="markdown"
    )


class GenerateTestsRequestSerializer(serializers.Serializer):
    """Request to generate unit tests."""

    chunk_id = serializers.UUIDField()
    framework = serializers.ChoiceField(
        choices=["auto", "pytest", "jest", "vitest", "junit", "go"],
        default="auto",
    )


class DetectBugsRequestSerializer(serializers.Serializer):
    """Request to detect bugs."""

    chunk_id = serializers.UUIDField()


class AIFeatureResponseSerializer(serializers.Serializer):
    """Response from any AI feature."""

    content = serializers.CharField()
    feature = serializers.CharField()
    chunk_id = serializers.CharField(allow_null=True)
    metadata = serializers.DictField()
