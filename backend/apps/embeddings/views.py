"""
Views for the embeddings app.

Provides semantic search API.
"""

import logging
import time

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.repositories.models import Repository

from .serializers import SearchRequestSerializer, SearchResultSerializer
from .services.search import SemanticSearchService

logger = logging.getLogger(__name__)


class SemanticSearchView(APIView):
    """
    POST /api/v1/embeddings/search/

    Perform semantic code search across repositories.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SearchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data["query"]
        repository_ids = serializer.validated_data["repository_ids"]
        filters = serializer.validated_data.get("filters", {})
        limit = serializer.validated_data.get("limit", 10)

        # Verify user owns all requested repositories
        owned_repos = Repository.objects.filter(
            id__in=repository_ids,
            owner=request.user,
        ).values_list("id", flat=True)

        if len(owned_repos) != len(repository_ids):
            return Response(
                {
                    "status": "error",
                    "message": "You do not have access to one or more repositories.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Perform search
        start_time = time.time()
        search_service = SemanticSearchService()

        try:
            results = search_service.search(
                query=query,
                repository_ids=[str(rid) for rid in repository_ids],
                limit=limit,
                filters=filters,
            )
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return Response(
                {"status": "error", "message": "Search failed. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        query_time_ms = round((time.time() - start_time) * 1000)

        result_serializer = SearchResultSerializer(results, many=True)

        return Response(
            {
                "status": "success",
                "data": {
                    "results": result_serializer.data,
                    "total": len(results),
                    "query_time_ms": query_time_ms,
                },
            }
        )
