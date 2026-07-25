"""Views for the notifications app."""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class NotificationListView(APIView):
    """List notifications for the current user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # TODO: Implement notification listing
        return Response({"results": []}, status=status.HTTP_200_OK)


class MarkReadView(APIView):
    """Mark a notification as read."""

    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        # TODO: Implement mark as read
        return Response(
            {"message": "Notification marked as read"},
            status=status.HTTP_200_OK,
        )
