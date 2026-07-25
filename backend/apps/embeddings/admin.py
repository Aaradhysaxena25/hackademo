"""Admin configuration for embeddings app."""

from django.contrib import admin

from .models import CodeChunk


@admin.register(CodeChunk)
class CodeChunkAdmin(admin.ModelAdmin):
    """Admin for the CodeChunk model."""

    list_display = ("indexed_file", "start_line", "end_line", "chunk_type", "created_at")
    list_filter = ("chunk_type",)
    search_fields = ("content", "indexed_file__file_path")
    ordering = ("-created_at",)
