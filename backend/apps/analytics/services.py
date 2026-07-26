"""
Analytics services for CodePilot.

Provides repository metrics calculation and usage tracking.
"""

import logging
from datetime import date, timedelta

from django.db.models import Count, Sum
from django.utils import timezone

from apps.chat.models import Conversation, Message
from apps.embeddings.models import CodeChunk
from apps.repositories.models import Repository, RepositoryFile

from .models import DailyUsageStats, UserActivity

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for computing analytics and metrics."""

    def get_user_dashboard_stats(self, user) -> dict:
        """Get overview stats for the user's dashboard."""
        repos = Repository.objects.filter(owner=user)
        conversations = Conversation.objects.filter(user=user, is_archived=False)
        messages = Message.objects.filter(conversation__user=user)
        activities = UserActivity.objects.filter(user=user)

        return {
            "total_repositories": repos.count(),
            "ready_repositories": repos.filter(status="ready").count(),
            "total_conversations": conversations.count(),
            "total_messages": messages.count(),
            "total_searches": activities.filter(action="search").count(),
            "total_files_indexed": repos.aggregate(total=Sum("total_files"))["total"] or 0,
            "total_chunks": repos.aggregate(total=Sum("total_chunks"))["total"] or 0,
        }

    def get_repository_analytics(self, repository: Repository) -> dict:
        """Get detailed analytics for a single repository."""
        files = RepositoryFile.objects.filter(repository=repository)
        chunks = CodeChunk.objects.filter(repository=repository)
        conversations = Conversation.objects.filter(repository=repository)

        # Language breakdown
        language_stats = (
            files.values("language")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        languages = {item["language"]: item["count"] for item in language_stats if item["language"]}

        # Embedding coverage
        total_chunks = chunks.count()
        embedded_chunks = chunks.filter(embedding__isnull=False).count()
        coverage = (embedded_chunks / total_chunks * 100) if total_chunks > 0 else 0

        return {
            "repository_id": str(repository.id),
            "name": repository.name,
            "status": repository.status,
            "total_files": repository.total_files,
            "total_chunks": total_chunks,
            "total_size_bytes": repository.total_size_bytes,
            "languages": languages,
            "embedding_coverage": round(coverage, 1),
            "total_conversations": conversations.count(),
            "total_messages": Message.objects.filter(conversation__repository=repository).count(),
            "last_indexed_at": repository.last_indexed_at,
        }

    def get_usage_stats(self, user, days: int = 30) -> dict:
        """Get usage statistics for the last N days."""
        since = timezone.now() - timedelta(days=days)

        daily_stats = (
            DailyUsageStats.objects.filter(user=user, date__gte=since.date())
            .order_by("date")
        )

        return {
            "period_days": days,
            "daily_stats": [
                {
                    "date": str(stat.date),
                    "queries": stat.queries_count,
                    "tokens": stat.tokens_used,
                }
                for stat in daily_stats
            ],
            "totals": {
                "queries": sum(s.queries_count for s in daily_stats),
                "tokens": sum(s.tokens_used for s in daily_stats),
                "repositories_indexed": sum(s.repositories_indexed for s in daily_stats),
            },
        }


class ActivityTracker:
    """Tracks user actions for analytics."""

    @staticmethod
    def track(user, action: str, resource_type: str = "", resource_id=None, metadata: dict | None = None):
        """Log a user activity."""
        UserActivity.objects.create(
            user=user,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            metadata=metadata or {},
        )

    @staticmethod
    def increment_daily_stat(user, field: str, amount: int = 1):
        """Increment a daily usage stat."""
        today = date.today()
        stat, _ = DailyUsageStats.objects.get_or_create(
            user=user, date=today
        )
        current = getattr(stat, field, 0)
        setattr(stat, field, current + amount)
        stat.save(update_fields=[field])
