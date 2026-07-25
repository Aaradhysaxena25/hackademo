"""
Semantic search service.

Performs vector similarity search across code chunks.
Uses cosine similarity with numpy for SQLite/dev mode.
In production with pgvector, this would use SQL-level vector operations.
"""

import logging
from dataclasses import dataclass
from typing import List

import numpy as np

from apps.embeddings.models import CodeChunk

from .generator import EmbeddingGenerator

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Represents a single search result."""

    chunk_id: str
    content: str
    file_path: str
    symbol_name: str | None
    chunk_type: str
    start_line: int
    end_line: int
    language: str
    relevance_score: float
    repository_id: str


class SemanticSearchService:
    """
    Performs semantic code search using vector similarity.

    In development (SQLite), loads embeddings into memory and computes
    cosine similarity. In production (PostgreSQL+pgvector), would use
    the database's native vector operations.
    """

    def __init__(self):
        self.generator = EmbeddingGenerator()

    def search(
        self,
        query: str,
        repository_ids: List[str],
        limit: int = 10,
        min_score: float = 0.3,
        filters: dict | None = None,
    ) -> List[SearchResult]:
        """
        Search for code chunks semantically similar to the query.

        Args:
            query: Natural language search query
            repository_ids: List of repository UUIDs to search within
            limit: Maximum number of results to return
            min_score: Minimum similarity score threshold
            filters: Optional filters (language, chunk_type, etc.)

        Returns:
            List of SearchResult objects sorted by relevance
        """
        # Generate query embedding
        query_embedding = self.generator.generate_embedding(query)

        # Fetch chunks with embeddings from target repositories
        queryset = CodeChunk.objects.filter(
            repository_id__in=repository_ids,
            embedding__isnull=False,
        )

        # Apply filters
        if filters:
            if filters.get("languages"):
                queryset = queryset.filter(
                    metadata__language__in=filters["languages"]
                )
            if filters.get("chunk_types"):
                queryset = queryset.filter(chunk_type__in=filters["chunk_types"])

        # Load chunks and compute similarities
        chunks = list(queryset.values(
            "id", "content", "start_line", "end_line",
            "chunk_type", "metadata", "embedding", "repository_id",
        ))

        if not chunks:
            return []

        # Compute cosine similarity for each chunk
        results = []
        query_vec = np.array(query_embedding)

        for chunk in chunks:
            if not chunk["embedding"]:
                continue

            chunk_vec = np.array(chunk["embedding"])
            similarity = float(np.dot(query_vec, chunk_vec))

            if similarity >= min_score:
                metadata = chunk["metadata"] or {}
                results.append(
                    SearchResult(
                        chunk_id=str(chunk["id"]),
                        content=chunk["content"],
                        file_path=metadata.get("file_path", ""),
                        symbol_name=metadata.get("symbol_name"),
                        chunk_type=chunk["chunk_type"] or "block",
                        start_line=chunk["start_line"],
                        end_line=chunk["end_line"],
                        language=metadata.get("language", ""),
                        relevance_score=round(similarity, 4),
                        repository_id=str(chunk["repository_id"]),
                    )
                )

        # Sort by relevance score descending
        results.sort(key=lambda r: r.relevance_score, reverse=True)

        return results[:limit]

    def search_for_rag(
        self,
        query: str,
        repository_id: str,
        limit: int = 5,
    ) -> List[SearchResult]:
        """
        Search specifically for RAG context retrieval.

        Uses a lower threshold and returns more context-rich results.

        Args:
            query: User's question
            repository_id: Single repository to search
            limit: Number of context chunks to retrieve

        Returns:
            List of most relevant SearchResult objects
        """
        return self.search(
            query=query,
            repository_ids=[repository_id],
            limit=limit,
            min_score=0.2,  # Lower threshold for RAG
        )
