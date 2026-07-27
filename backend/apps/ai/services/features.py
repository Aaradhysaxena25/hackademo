"""
AI feature services — explain, generate docs, generate tests, detect bugs.

Each feature uses a specialized prompt and the LLM provider.
"""

import logging
from dataclasses import dataclass, field

from apps.embeddings.models import CodeChunk

from .llm_provider import LLMProvider, get_llm_provider
from .prompts import (
    DETECT_BUGS_PROMPT,
    EXPLAIN_PROMPT,
    GENERATE_DOCS_PROMPT,
    GENERATE_TESTS_PROMPT,
)

logger = logging.getLogger(__name__)


@dataclass
class AIFeatureResponse:
    """Response from an AI feature."""

    content: str
    feature: str
    chunk_id: str | None = None
    metadata: dict = field(default_factory=dict)


class AIFeatureService:
    """
    Service for AI-powered code features.

    Provides: explain, generate docs, generate tests, detect bugs.
    """

    def __init__(self, llm_provider: LLMProvider | None = None, provider_name: str = "openai"):
        from .llm_provider import get_default_provider

        if llm_provider:
            self.llm = llm_provider
        else:
            self.llm = get_default_provider()

    def explain_code(self, chunk_id: str, detail_level: str = "detailed") -> AIFeatureResponse:
        """
        Generate a plain-English explanation of a code chunk.

        Args:
            chunk_id: UUID of the CodeChunk to explain
            detail_level: 'brief' or 'detailed'
        """
        chunk = self._get_chunk(chunk_id)
        metadata = chunk.metadata or {}

        user_content = self._build_code_context(chunk, metadata)
        if detail_level == "brief":
            user_content += "\n\nProvide a brief 2-3 sentence explanation."
        else:
            user_content += "\n\nProvide a detailed explanation."

        messages = [
            {"role": "system", "content": EXPLAIN_PROMPT},
            {"role": "user", "content": user_content},
        ]

        content = self.llm.generate(messages)

        return AIFeatureResponse(
            content=content,
            feature="explain",
            chunk_id=chunk_id,
            metadata={"detail_level": detail_level, "language": metadata.get("language", "")},
        )

    def generate_docs(self, chunk_id: str, doc_format: str = "markdown") -> AIFeatureResponse:
        """
        Generate documentation for a code chunk.

        Args:
            chunk_id: UUID of the CodeChunk
            doc_format: Output format ('markdown', 'docstring')
        """
        chunk = self._get_chunk(chunk_id)
        metadata = chunk.metadata or {}

        user_content = self._build_code_context(chunk, metadata)
        user_content += f"\n\nGenerate {doc_format} documentation for this code."

        messages = [
            {"role": "system", "content": GENERATE_DOCS_PROMPT},
            {"role": "user", "content": user_content},
        ]

        content = self.llm.generate(messages)

        return AIFeatureResponse(
            content=content,
            feature="generate_docs",
            chunk_id=chunk_id,
            metadata={"format": doc_format, "language": metadata.get("language", "")},
        )

    def generate_tests(
        self, chunk_id: str, framework: str = "auto"
    ) -> AIFeatureResponse:
        """
        Generate unit tests for a code chunk.

        Args:
            chunk_id: UUID of the CodeChunk
            framework: Test framework ('pytest', 'jest', 'vitest', 'auto')
        """
        chunk = self._get_chunk(chunk_id)
        metadata = chunk.metadata or {}
        language = metadata.get("language", "")

        # Auto-detect framework
        if framework == "auto":
            framework = self._detect_test_framework(language)

        user_content = self._build_code_context(chunk, metadata)
        user_content += f"\n\nGenerate unit tests using {framework}."

        messages = [
            {"role": "system", "content": GENERATE_TESTS_PROMPT},
            {"role": "user", "content": user_content},
        ]

        content = self.llm.generate(messages)

        return AIFeatureResponse(
            content=content,
            feature="generate_tests",
            chunk_id=chunk_id,
            metadata={"framework": framework, "language": language},
        )

    def detect_bugs(self, chunk_id: str) -> AIFeatureResponse:
        """
        Analyze a code chunk for potential bugs and issues.

        Args:
            chunk_id: UUID of the CodeChunk
        """
        chunk = self._get_chunk(chunk_id)
        metadata = chunk.metadata or {}

        user_content = self._build_code_context(chunk, metadata)
        user_content += "\n\nAnalyze this code for potential bugs, security issues, and anti-patterns."

        messages = [
            {"role": "system", "content": DETECT_BUGS_PROMPT},
            {"role": "user", "content": user_content},
        ]

        content = self.llm.generate(messages)

        return AIFeatureResponse(
            content=content,
            feature="detect_bugs",
            chunk_id=chunk_id,
            metadata={"language": metadata.get("language", "")},
        )

    def _get_chunk(self, chunk_id: str) -> CodeChunk:
        """Retrieve a code chunk by ID."""
        try:
            return CodeChunk.objects.get(id=chunk_id)
        except CodeChunk.DoesNotExist:
            raise ValueError(f"Code chunk not found: {chunk_id}")

    def _build_code_context(self, chunk: CodeChunk, metadata: dict) -> str:
        """Build the code context string for the LLM."""
        parts = []

        file_path = metadata.get("file_path", "unknown")
        language = metadata.get("language", "")
        symbol_name = metadata.get("symbol_name", "")

        parts.append(f"File: {file_path}")
        if language:
            parts.append(f"Language: {language}")
        if symbol_name:
            parts.append(f"Symbol: {symbol_name}")
        parts.append(f"Lines: {chunk.start_line}-{chunk.end_line}")

        header = " | ".join(parts)
        return f"{header}\n\n```{language}\n{chunk.content}\n```"

    def _detect_test_framework(self, language: str) -> str:
        """Auto-detect the appropriate test framework for a language."""
        framework_map = {
            "python": "pytest",
            "javascript": "vitest",
            "typescript": "vitest",
            "java": "junit",
            "go": "testing",
            "rust": "built-in",
            "ruby": "rspec",
            "php": "phpunit",
            "csharp": "xunit",
        }
        return framework_map.get(language, "appropriate testing framework")
