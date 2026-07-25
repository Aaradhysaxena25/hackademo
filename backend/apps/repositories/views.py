"""
Views for the repositories app.

Handles CRUD operations for repositories and file browsing.
"""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.pagination import StandardResultsSetPagination

from .models import Repository, RepositoryFile
from .permissions import IsRepositoryOwner
from .serializers import (
    RepositoryCreateSerializer,
    RepositoryDetailSerializer,
    RepositoryFileSerializer,
    RepositoryListSerializer,
)


class RepositoryListView(APIView):
    """
    GET  /api/v1/repositories/       — List user's repositories
    POST /api/v1/repositories/       — Create/import a repository
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Repository.objects.filter(owner=request.user)

        # Filtering
        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)

        # Ordering
        ordering = request.query_params.get("ordering", "-created_at")
        allowed_orderings = ["created_at", "-created_at", "name", "-name", "-last_indexed_at"]
        if ordering in allowed_orderings:
            queryset = queryset.order_by(ordering)

        # Pagination
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = RepositoryListSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = RepositoryCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        repository = serializer.save()

        return Response(
            {
                "status": "success",
                "data": RepositoryDetailSerializer(repository).data,
                "message": "Repository created successfully.",
            },
            status=status.HTTP_201_CREATED,
        )


class RepositoryDetailView(APIView):
    """
    GET    /api/v1/repositories/{id}/  — Get repository detail
    PATCH  /api/v1/repositories/{id}/  — Update repository
    DELETE /api/v1/repositories/{id}/  — Delete repository
    """

    permission_classes = [IsAuthenticated, IsRepositoryOwner]

    def get_object(self, pk, user):
        repo = get_object_or_404(Repository, pk=pk)
        self.check_object_permissions(self.request, repo)
        return repo

    def get(self, request, pk):
        repo = self.get_object(pk, request.user)
        return Response(
            {
                "status": "success",
                "data": RepositoryDetailSerializer(repo).data,
            }
        )

    def patch(self, request, pk):
        repo = self.get_object(pk, request.user)
        # Only allow updating description and name
        allowed_fields = {"name", "description"}
        update_data = {k: v for k, v in request.data.items() if k in allowed_fields}

        for field, value in update_data.items():
            setattr(repo, field, value)
        repo.save(update_fields=list(update_data.keys()) + ["updated_at"])

        return Response(
            {
                "status": "success",
                "data": RepositoryDetailSerializer(repo).data,
            }
        )

    def delete(self, request, pk):
        repo = self.get_object(pk, request.user)
        repo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RepositoryReindexView(APIView):
    """
    POST /api/v1/repositories/{id}/reindex/  — Trigger re-indexing
    """

    permission_classes = [IsAuthenticated, IsRepositoryOwner]

    def post(self, request, pk):
        repo = get_object_or_404(Repository, pk=pk, owner=request.user)
        self.check_object_permissions(request, repo)

        if repo.status == "indexing":
            return Response(
                {"status": "error", "message": "Repository is already being indexed."},
                status=status.HTTP_409_CONFLICT,
            )

        # Set status to pending (will be picked up by indexing task later)
        repo.status = "pending"
        repo.save(update_fields=["status", "updated_at"])

        # TODO: Dispatch Celery indexing task
        # from apps.indexing.tasks import index_repository_task
        # index_repository_task.delay(str(repo.id))

        return Response(
            {
                "status": "success",
                "message": "Re-indexing started.",
                "data": {"repository_id": str(repo.id), "status": repo.status},
            },
            status=status.HTTP_202_ACCEPTED,
        )


class RepositoryFilesView(APIView):
    """
    GET /api/v1/repositories/{id}/files/  — Browse repository files
    """

    permission_classes = [IsAuthenticated, IsRepositoryOwner]

    def get(self, request, pk):
        repo = get_object_or_404(Repository, pk=pk, owner=request.user)
        self.check_object_permissions(request, repo)

        queryset = RepositoryFile.objects.filter(repository=repo)

        # Filter by path prefix (directory browsing)
        path_prefix = request.query_params.get("path", "")
        if path_prefix:
            queryset = queryset.filter(file_path__startswith=path_prefix)

        # Filter by language
        language = request.query_params.get("language")
        if language:
            queryset = queryset.filter(language=language)

        # Search by filename
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(file_name__icontains=search)

        # Pagination
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = RepositoryFileSerializer(page, many=True)

        return paginator.get_paginated_response(serializer.data)
