"""
Celery tasks for embedding generation.
"""

import logging

from celery import shared_task

from apps.embeddings.models import CodeChunk

from .services.generator import EmbeddingGenerator

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def generate_embeddings_task(self, repository_id: str):
    """
    Generate embeddings for all chunks in a repository that don't have them yet.

    Args:
        repository_id: UUID of the repository
    """
    generator = EmbeddingGenerator()

    # Get chunks without embeddings
    chunks = CodeChunk.objects.filter(
        repository_id=repository_id,
        embedding__isnull=True,
    )

    total = chunks.count()
    if total == 0:
        logger.info(f"No chunks to embed for repository {repository_id}")
        return

    logger.info(f"Generating embeddings for {total} chunks in repository {repository_id}")

    # Process in batches
    batch_size = 32
    processed = 0
    chunk_list = list(chunks.values_list("id", "content", "metadata"))

    for i in range(0, len(chunk_list), batch_size):
        batch = chunk_list[i : i + batch_size]

        # Prepare augmented texts
        texts = []
        for _, content, metadata in batch:
            augmented = generator.augment_text(content, metadata or {})
            texts.append(augmented)

        try:
            # Generate embeddings for batch
            embeddings = generator.generate_embeddings_batch(texts)

            # Update chunks with embeddings
            for j, (chunk_id, _, _) in enumerate(batch):
                CodeChunk.objects.filter(id=chunk_id).update(
                    embedding=embeddings[j],
                    embedding_model=generator.model_name,
                )

            processed += len(batch)
            logger.info(f"Embedded {processed}/{total} chunks")

        except Exception as e:
            logger.error(f"Error generating embeddings for batch: {e}")
            if self.request.retries < self.max_retries:
                raise self.retry(exc=e)

    logger.info(
        f"Embedding generation complete for repository {repository_id}: "
        f"{processed} chunks embedded"
    )
