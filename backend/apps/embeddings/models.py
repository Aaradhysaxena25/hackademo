"""
Embedding models for CodePilot.
"""

from django.db import models

from apps.common.models import BaseModel


class CodeChunk(BaseModel):
    """Represents a chunk of code with its embedding vector."""

    indexed_file = models.ForeignKey(
        "indexing.IndexedFile",
        on_delete=models.CASCADE,
        related_name="code_chunks",
    )
    repository = models.ForeignKey(
        "repositories.Repository",
        on_delete=models.CASCADE,
        related_name="code_chunks",
    )
    content = models.TextField()
    start_line = models.IntegerField()
    end_line = models.IntegerField()
    chunk_type = models.CharField(max_length=50, blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)

    # Embedding vector stored as JSON list of floats.
    # In production with PostgreSQL+pgvector, this would be:
    #   from pgvector.django import VectorField
    #   embedding = VectorField(dimensions=384)
    embedding = models.JSONField(null=True, blank=True, default=None)
    embedding_model = models.CharField(max_length=100, default="all-MiniLM-L6-v2")

    class Meta:
        db_table = "embeddings_code_chunk"
        verbose_name = "Code Chunk"
        verbose_name_plural = "Code Chunks"
        ordering = ["indexed_file", "start_line"]

    def __str__(self):
        file_path = self.metadata.get("file_path", "unknown")
        return f"Chunk({file_path}:{self.start_line}-{self.end_line})"

    @property
    def has_embedding(self) -> bool:
        return self.embedding is not None and len(self.embedding) > 0
