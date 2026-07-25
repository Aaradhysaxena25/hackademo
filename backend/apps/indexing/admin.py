"""Admin configuration for indexing app."""

from django.contrib import admin

from .models import IndexedFile, IndexingJob


@admin.register(IndexingJob)
class IndexingJobAdmin(admin.ModelAdmin):
    """Admin for the IndexingJob model."""

    list_display = ("repository", "status", "total_files", "processed_files", "created_at")
    list_filter = ("status",)
    search_fields = ("repository__name",)
    ordering = ("-created_at",)


@admin.register(IndexedFile)
class IndexedFileAdmin(admin.ModelAdmin):
    """Admin for the IndexedFile model."""

    list_display = ("file_path", "repository", "file_type", "size_bytes")
    list_filter = ("file_type",)
    search_fields = ("file_path", "file_name")
    ordering = ("file_path",)
