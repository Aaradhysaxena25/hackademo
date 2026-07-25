"""Views for the analytics app."""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class UsageStatsView(APIView):
    """Get usage statistics for the current user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # TODO: Implement usage stats
        return Response(
            {"message": "Usage stats endpoint"},
            status=status.HTTP_501_NOT_IMPLEMENTED,
        )


class ActivityLogView(APIView):
    """Get recent activity log for the current user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # TODO: Implement activity log
        return Response({"results": []}, status=status.HTTP_200_OK)
