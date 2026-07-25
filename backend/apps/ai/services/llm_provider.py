"""
LLM Provider abstraction.

Supports OpenAI-compatible APIs and Ollama for local inference.
"""

import logging
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generator

from django.conf import settings

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, messages: list[dict], **kwargs) -> str:
        """Generate a response synchronously."""
        pass

    @abstractmethod
    def generate_stream(self, messages: list[dict], **kwargs) -> Generator[str, None, None]:
        """Generate a response as a stream of tokens."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI-compatible API provider."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        base_url: str | None = None,
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model
        self.base_url = base_url
        self.max_tokens = max_tokens
        self.temperature = temperature

    def _get_client(self):
        from openai import OpenAI

        kwargs = {"api_key": self.api_key}
        if self.base_url:
            kwargs["base_url"] = self.base_url
        return OpenAI(**kwargs)

    def generate(self, messages: list[dict], **kwargs) -> str:
        """Generate a complete response."""
        client = self._get_client()

        response = client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=messages,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", self.temperature),
        )

        return response.choices[0].message.content or ""

    def generate_stream(self, messages: list[dict], **kwargs) -> Generator[str, None, None]:
        """Generate a streaming response."""
        client = self._get_client()

        stream = client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=messages,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", self.temperature),
            stream=True,
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "codellama:7b",
        max_tokens: int = 2048,
        temperature: float = 0.1,
    ):
        self.base_url = base_url
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def generate(self, messages: list[dict], **kwargs) -> str:
        """Generate a complete response via Ollama."""
        import requests

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": kwargs.get("model", self.model),
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": kwargs.get("max_tokens", self.max_tokens),
                    "temperature": kwargs.get("temperature", self.temperature),
                },
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json().get("message", {}).get("content", "")

    def generate_stream(self, messages: list[dict], **kwargs) -> Generator[str, None, None]:
        """Generate a streaming response via Ollama."""
        import requests

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": kwargs.get("model", self.model),
                "messages": messages,
                "stream": True,
                "options": {
                    "num_predict": kwargs.get("max_tokens", self.max_tokens),
                    "temperature": kwargs.get("temperature", self.temperature),
                },
            },
            stream=True,
            timeout=60,
        )
        response.raise_for_status()

        import json

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                content = data.get("message", {}).get("content", "")
                if content:
                    yield content


class MockProvider(LLMProvider):
    """Mock LLM provider for testing."""

    def __init__(self, response: str = "This is a mock AI response."):
        self.response = response

    def generate(self, messages: list[dict], **kwargs) -> str:
        return self.response

    def generate_stream(self, messages: list[dict], **kwargs) -> Generator[str, None, None]:
        for word in self.response.split():
            yield word + " "


def get_llm_provider(provider_name: str = "openai", **kwargs) -> LLMProvider:
    """
    Factory function to get an LLM provider instance.

    Args:
        provider_name: One of 'openai', 'ollama', 'mock'
        **kwargs: Provider-specific configuration

    Returns:
        LLMProvider instance
    """
    providers = {
        "openai": OpenAIProvider,
        "ollama": OllamaProvider,
        "mock": MockProvider,
    }

    provider_class = providers.get(provider_name)
    if not provider_class:
        raise ValueError(f"Unknown LLM provider: {provider_name}")

    return provider_class(**kwargs)
