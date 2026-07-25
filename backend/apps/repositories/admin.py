"""Admin configuration for repositories app."""

from django.contrib import admin

from .models import Repository, RepositoryFile


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    """Admin for the Repository model."""

    list_display = ("name", "owner", "source_type", "status", "total_files", "created_at")
    list_filter = ("status", "source_type")
    search_fields = ("name", "owner__email")
    ordering = ("-created_at",)


@admin.register(RepositoryFile)
class RepositoryFileAdmin(admin.ModelAdmin):
    """Admin for the RepositoryFile model."""

    list_display = ("file_path", "repository", "language", "size_bytes", "line_count")
    list_filter = ("language",)
    search_fields = ("file_path", "file_name")
    ordering = ("file_path",)
