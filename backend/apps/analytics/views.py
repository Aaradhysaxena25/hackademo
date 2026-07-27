"""
Views for the analytics app.
"""

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.repositories.models import Repository

from .models import UserActivity
from .serializers import UserActivitySerializer
from .services import AnalyticsService


class DashboardStatsView(APIView):
    """
    GET /api/v1/analytics/dashboard/

    Get overview stats for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        service = AnalyticsService()
        stats = service.get_user_dashboard_stats(request.user)
        return Response({"status": "success", "data": stats})


class RepositoryAnalyticsView(APIView):
    """
    GET /api/v1/analytics/repositories/{id}/

    Get detailed analytics for a specific repository.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        repo = get_object_or_404(Repository, pk=pk, owner=request.user)
        service = AnalyticsService()
        analytics = service.get_repository_analytics(repo)
        return Response({"status": "success", "data": analytics})


class UsageStatsView(APIView):
    """
    GET /api/v1/analytics/usage/

    Get usage statistics for the last N days.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        days = min(days, 90)  # Cap at 90 days

        service = AnalyticsService()
        stats = service.get_usage_stats(request.user, days=days)
        return Response({"status": "success", "data": stats})


class ActivityLogView(APIView):
    """
    GET /api/v1/analytics/activity/

    Get recent activity log.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        activities = UserActivity.objects.filter(user=request.user)[:50]
        serializer = UserActivitySerializer(activities, many=True)
        return Response({"status": "success", "data": serializer.data})
