"""
RAG (Retrieval-Augmented Generation) pipeline.

Orchestrates: embed query → search → build context → generate response
"""

import logging
from dataclasses import dataclass, field
from typing import Generator

from apps.embeddings.services.search import SemanticSearchService

from .llm_provider import LLMProvider, get_llm_provider
from .prompt_builder import PromptBuilder

logger = logging.getLogger(__name__)


@dataclass
class RAGResponse:
    """Complete response from the RAG pipeline."""

    content: str
    sources: list[dict] = field(default_factory=list)
    token_count: int = 0
    model_used: str = ""


class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline.

    1. Embeds the user query
    2. Searches for relevant code chunks
    3. Builds a prompt with code context
    4. Generates a response using the LLM
    """

    def __init__(
        self,
        llm_provider: LLMProvider | None = None,
        provider_name: str = "openai",
    ):
        self.search_service = SemanticSearchService()
        self.prompt_builder = PromptBuilder()
        self.llm = llm_provider or get_llm_provider(provider_name)

    def generate_response(
        self,
        query: str,
        repository_id: str,
        conversation_history: list[dict] | None = None,
        repository_name: str = "",
        num_chunks: int = 5,
    ) -> RAGResponse:
        """
        Execute the full RAG pipeline and return a response.

        Args:
            query: User's question
            repository_id: Repository to search for context
            conversation_history: Previous messages for context
            repository_name: Name of the repo for the system prompt
            num_chunks: Number of code chunks to retrieve

        Returns:
            RAGResponse with content, sources, and metadata
        """
        # Step 1: Retrieve relevant code chunks
        search_results = self.search_service.search_for_rag(
            query=query,
            repository_id=repository_id,
            limit=num_chunks,
        )

        # Step 2: Format context chunks
        context_chunks = [
            {
                "file_path": r.file_path,
                "start_line": r.start_line,
                "end_line": r.end_line,
                "language": r.language,
                "content": r.content,
                "relevance_score": r.relevance_score,
                "chunk_type": r.chunk_type,
                "symbol_name": r.symbol_name,
            }
            for r in search_results
        ]

        # Step 3: Build prompt
        messages = self.prompt_builder.build_messages(
            user_query=query,
            context_chunks=context_chunks if context_chunks else None,
            conversation_history=conversation_history,
            repository_name=repository_name,
        )

        # Step 4: Generate response
        try:
            content = self.llm.generate(messages)
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            content = "I'm sorry, I encountered an error while generating a response. Please try again."

        # Step 5: Format sources for the response
        sources = [
            {
                "file_path": r.file_path,
                "start_line": r.start_line,
                "end_line": r.end_line,
                "chunk_type": r.chunk_type,
                "relevance_score": r.relevance_score,
            }
            for r in search_results
        ]

        return RAGResponse(
            content=content,
            sources=sources,
            token_count=len(content.split()),  # Approximate
            model_used=getattr(self.llm, "model", "unknown"),
        )

    def generate_response_stream(
        self,
        query: str,
        repository_id: str,
        conversation_history: list[dict] | None = None,
        repository_name: str = "",
        num_chunks: int = 5,
    ) -> Generator[dict, None, None]:
        """
        Execute RAG pipeline with streaming response.

        Yields dicts with type: 'chunk' (content), 'sources', or 'done'.
        """
        # Step 1-3: Same as non-streaming
        search_results = self.search_service.search_for_rag(
            query=query,
            repository_id=repository_id,
            limit=num_chunks,
        )

        context_chunks = [
            {
                "file_path": r.file_path,
                "start_line": r.start_line,
                "end_line": r.end_line,
                "language": r.language,
                "content": r.content,
                "relevance_score": r.relevance_score,
                "chunk_type": r.chunk_type,
                "symbol_name": r.symbol_name,
            }
            for r in search_results
        ]

        messages = self.prompt_builder.build_messages(
            user_query=query,
            context_chunks=context_chunks if context_chunks else None,
            conversation_history=conversation_history,
            repository_name=repository_name,
        )

        # Step 4: Stream response
        full_content = ""
        try:
            for token in self.llm.generate_stream(messages):
                full_content += token
                yield {"type": "chunk", "content": token}
        except Exception as e:
            logger.error(f"LLM streaming failed: {e}")
            yield {"type": "chunk", "content": "Error generating response."}

        # Step 5: Send sources after streaming completes
        sources = [
            {
                "file_path": r.file_path,
                "start_line": r.start_line,
                "end_line": r.end_line,
                "chunk_type": r.chunk_type,
                "relevance_score": r.relevance_score,
            }
            for r in search_results
        ]

        yield {"type": "sources", "sources": sources}
        yield {
            "type": "done",
            "token_count": len(full_content.split()),
            "model_used": getattr(self.llm, "model", "unknown"),
        }
