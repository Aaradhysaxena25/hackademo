"""
Enums and constants used across the CodePilot application.
"""

from django.db import models


class RepositoryStatus(models.TextChoices):
    """Status of a repository in the system."""

    PENDING = "pending", "Pending"
    CLONING = "cloning", "Cloning"
    INDEXING = "indexing", "Indexing"
    READY = "ready", "Ready"
    ERROR = "error", "Error"
    ARCHIVED = "archived", "Archived"


class IndexingStatus(models.TextChoices):
    """Status of an indexing job."""

    QUEUED = "queued", "Queued"
    PROCESSING = "processing", "Processing"
    COMPLETED = "completed", "Completed"
    FAILED = "failed", "Failed"
    CANCELLED = "cancelled", "Cancelled"


class FileType(models.TextChoices):
    """Supported file types for indexing."""

    PYTHON = "python", "Python"
    JAVASCRIPT = "javascript", "JavaScript"
    TYPESCRIPT = "typescript", "TypeScript"
    JAVA = "java", "Java"
    GO = "go", "Go"
    RUST = "rust", "Rust"
    CPP = "cpp", "C++"
    C = "c", "C"
    RUBY = "ruby", "Ruby"
    PHP = "php", "PHP"
    MARKDOWN = "markdown", "Markdown"
    OTHER = "other", "Other"


class ChatMessageRole(models.TextChoices):
    """Role of a chat message sender."""

    USER = "user", "User"
    ASSISTANT = "assistant", "Assistant"
    SYSTEM = "system", "System"


class SubscriptionPlan(models.TextChoices):
    """User subscription plans."""

    FREE = "free", "Free"
    PRO = "pro", "Pro"
    ENTERPRISE = "enterprise", "Enterprise"


class NotificationType(models.TextChoices):
    """Types of notifications."""

    INDEXING_COMPLETE = "indexing_complete", "Indexing Complete"
    INDEXING_FAILED = "indexing_failed", "Indexing Failed"
    REPOSITORY_ADDED = "repository_added", "Repository Added"
    SYSTEM = "system", "System"
