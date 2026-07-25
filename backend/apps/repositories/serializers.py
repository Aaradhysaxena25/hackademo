"""
Serializers for the repositories app.
"""

from rest_framework import serializers

from .models import Repository, RepositoryFile


class RepositoryListSerializer(serializers.ModelSerializer):
    """Serializer for repository list view."""

    class Meta:
        model = Repository
        fields = [
            "id",
            "name",
            "description",
            "source_type",
            "github_url",
            "default_branch",
            "status",
            "total_files",
            "total_chunks",
            "total_size_bytes",
            "languages",
            "last_indexed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class RepositoryDetailSerializer(serializers.ModelSerializer):
    """Serializer for repository detail view."""

    files_count = serializers.SerializerMethodField()

    class Meta:
        model = Repository
        fields = [
            "id",
            "name",
            "description",
            "source_type",
            "github_url",
            "default_branch",
            "status",
            "total_files",
            "total_chunks",
            "total_size_bytes",
            "languages",
            "last_indexed_at",
            "files_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_files_count(self, obj):
        return obj.files.count()


class RepositoryCreateSerializer(serializers.Serializer):
    """Serializer for creating a repository."""

    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, default="", allow_blank=True)
    source_type = serializers.ChoiceField(
        choices=Repository.SourceType.choices,
    )
    github_url = serializers.URLField(required=False, default="")
    default_branch = serializers.CharField(max_length=100, required=False, default="main")

    def validate_name(self, value):
        """Sanitize repository name."""
        import re

        value = value.strip()
        if not re.match(r"^[\w\-. ]+$", value):
            raise serializers.ValidationError(
                "Name can only contain letters, numbers, hyphens, underscores, dots, and spaces."
            )
        return value

    def validate_github_url(self, value):
        """Validate GitHub URL format if provided."""
        import re

        if value:
            pattern = r"^https://github\.com/[\w.\-]+/[\w.\-]+/?$"
            if not re.match(pattern, value):
                raise serializers.ValidationError("Invalid GitHub repository URL.")
        return value

    def validate(self, data):
        """Cross-field validation."""
        if data["source_type"] == Repository.SourceType.GITHUB and not data.get("github_url"):
            raise serializers.ValidationError(
                {"github_url": "GitHub URL is required for GitHub imports."}
            )
        return data

    def create(self, validated_data):
        owner = self.context["request"].user
        # Check repo limit (free tier: 5)
        repo_count = Repository.objects.filter(owner=owner).count()
        if repo_count >= 10:
            raise serializers.ValidationError(
                "You have reached the maximum number of repositories."
            )

        repository = Repository.objects.create(owner=owner, **validated_data)
        return repository


class RepositoryFileSerializer(serializers.ModelSerializer):
    """Serializer for repository files."""

    class Meta:
        model = RepositoryFile
        fields = [
            "id",
            "file_path",
            "file_name",
            "language",
            "size_bytes",
            "line_count",
        ]
        read_only_fields = fields
