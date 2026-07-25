"""
Views for the indexing app.
"""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import IndexingJob
from .serializers import IndexingJobSerializer


class IndexingJobDetailView(APIView):
    """
    GET /api/v1/indexing/jobs/{id}/  — Get indexing job status
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        job = get_object_or_404(IndexingJob, pk=pk)

        # Verify the user owns the repository
        if job.repository.owner_id != request.user.id:
            return Response(
                {"status": "error", "message": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(
            {
                "status": "success",
                "data": IndexingJobSerializer(job).data,
            }
        )


class RepositoryIndexingJobsView(APIView):
    """
    GET /api/v1/indexing/repositories/{repo_id}/jobs/  — List jobs for a repository
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, repo_id):
        jobs = IndexingJob.objects.filter(
            repository_id=repo_id,
            repository__owner=request.user,
        ).order_by("-created_at")[:10]

        return Response(
            {
                "status": "success",
                "data": IndexingJobSerializer(jobs, many=True).data,
            }
        )
