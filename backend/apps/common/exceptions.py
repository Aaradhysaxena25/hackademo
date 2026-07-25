"""
Custom exceptions for CodePilot.
"""

from rest_framework.exceptions import APIException


class ServiceUnavailableError(APIException):
    """Raised when an external service is unavailable."""

    status_code = 503
    default_detail = "Service temporarily unavailable, please try again later."
    default_code = "service_unavailable"


class RateLimitExceededError(APIException):
    """Raised when a rate limit is exceeded."""

    status_code = 429
    default_detail = "Rate limit exceeded. Please try again later."
    default_code = "rate_limit_exceeded"


class RepositoryNotFoundError(APIException):
    """Raised when a repository cannot be found."""

    status_code = 404
    default_detail = "Repository not found."
    default_code = "repository_not_found"


class IndexingError(APIException):
    """Raised when an indexing operation fails."""

    status_code = 500
    default_detail = "An error occurred during indexing."
    default_code = "indexing_error"


class EmbeddingError(APIException):
    """Raised when embedding generation fails."""

    status_code = 500
    default_detail = "An error occurred generating embeddings."
    default_code = "embedding_error"


class AIServiceError(APIException):
    """Raised when the AI service encounters an error."""

    status_code = 502
    default_detail = "AI service error."
    default_code = "ai_service_error"
