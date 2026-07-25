"""
Embedding generation service.

Generates vector embeddings for code chunks using Sentence Transformers.
"""

import logging
from typing import List

import numpy as np

logger = logging.getLogger(__name__)

# Model is loaded lazily on first use to avoid startup cost
_model = None
_model_name = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384


def _get_model():
    """Lazy-load the sentence transformer model."""
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer

            _model = SentenceTransformer(_model_name)
            logger.info(f"Loaded embedding model: {_model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    return _model


class EmbeddingGenerator:
    """
    Generates embeddings for code chunks using Sentence Transformers.

    Supports context augmentation (prepending file path + language) and
    batch processing for efficiency.
    """

    def __init__(self, batch_size: int = 32):
        self.batch_size = batch_size
        self.model_name = _model_name
        self.dimensions = EMBEDDING_DIMENSIONS

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text to embed

        Returns:
            List of floats representing the embedding vector
        """
        model = _get_model()
        embedding = model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embedding.tolist()

    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a batch of texts.

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        model = _get_model()
        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            embeddings = model.encode(
                batch,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
            all_embeddings.extend(embeddings.tolist())

        return all_embeddings

    def augment_text(self, content: str, metadata: dict) -> str:
        """
        Augment chunk content with contextual information for better embeddings.

        Prepends file path, language, and symbol name to improve retrieval quality.

        Args:
            content: Raw code content
            metadata: Chunk metadata dict

        Returns:
            Augmented text ready for embedding
        """
        parts = []

        file_path = metadata.get("file_path", "")
        if file_path:
            parts.append(f"File: {file_path}")

        language = metadata.get("language", "")
        if language:
            parts.append(f"Language: {language}")

        symbol_name = metadata.get("symbol_name", "")
        if symbol_name:
            parts.append(f"Symbol: {symbol_name}")

        prefix = " | ".join(parts)
        if prefix:
            return f"{prefix}\n\n{content}"
        return content

    def compute_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Compute cosine similarity between two vectors.

        Args:
            vec_a: First embedding vector
            vec_b: Second embedding vector

        Returns:
            Cosine similarity score (0 to 1 for normalized vectors)
        """
        a = np.array(vec_a)
        b = np.array(vec_b)

        # For normalized vectors, dot product = cosine similarity
        return float(np.dot(a, b))
