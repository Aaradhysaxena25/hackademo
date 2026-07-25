"""
Views for AI feature endpoints.

Provides: explain code, generate docs, generate tests, detect bugs.
"""

import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.embeddings.models import CodeChunk

from .serializers import (
    AIFeatureResponseSerializer,
    DetectBugsRequestSerializer,
    ExplainRequestSerializer,
    GenerateDocsRequestSerializer,
    GenerateTestsRequestSerializer,
)
from .services.features import AIFeatureService

logger = logging.getLogger(__name__)


class BaseAIFeatureView(APIView):
    """Base view for AI features with common validation."""

    permission_classes = [IsAuthenticated]

    def _validate_chunk_access(self, request, chunk_id: str) -> CodeChunk | None:
        """Verify the user owns the repository containing the chunk."""
        try:
            chunk = CodeChunk.objects.select_related(
                "repository"
            ).get(id=chunk_id)
        except CodeChunk.DoesNotExist:
            return None

        if chunk.repository.owner_id != request.user.id:
            return None

        return chunk


class ExplainCodeView(BaseAIFeatureView):
    """
    POST /api/v1/ai/explain/

    Generate a plain-English explanation of a code chunk.
    """

    def post(self, request):
        serializer = ExplainRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chunk_id = str(serializer.validated_data["chunk_id"])
        detail_level = serializer.validated_data["detail_level"]

        chunk = self._validate_chunk_access(request, chunk_id)
        if not chunk:
            return Response(
                {"status": "error", "message": "Code chunk not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            service = AIFeatureService()
            result = service.explain_code(chunk_id, detail_level)
            return Response(
                {"status": "success", "data": AIFeatureResponseSerializer(result).data}
            )
        except Exception as e:
            logger.error(f"Explain code failed: {e}")
            return Response(
                {"status": "error", "message": "Failed to generate explanation."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GenerateDocsView(BaseAIFeatureView):
    """
    POST /api/v1/ai/generate-docs/

    Generate documentation for a code chunk.
    """

    def post(self, request):
        serializer = GenerateDocsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chunk_id = str(serializer.validated_data["chunk_id"])
        doc_format = serializer.validated_data["format"]

        chunk = self._validate_chunk_access(request, chunk_id)
        if not chunk:
            return Response(
                {"status": "error", "message": "Code chunk not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            service = AIFeatureService()
            result = service.generate_docs(chunk_id, doc_format)
            return Response(
                {"status": "success", "data": AIFeatureResponseSerializer(result).data}
            )
        except Exception as e:
            logger.error(f"Generate docs failed: {e}")
            return Response(
                {"status": "error", "message": "Failed to generate documentation."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GenerateTestsView(BaseAIFeatureView):
    """
    POST /api/v1/ai/generate-tests/

    Generate unit tests for a code chunk.
    """

    def post(self, request):
        serializer = GenerateTestsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chunk_id = str(serializer.validated_data["chunk_id"])
        framework = serializer.validated_data["framework"]

        chunk = self._validate_chunk_access(request, chunk_id)
        if not chunk:
            return Response(
                {"status": "error", "message": "Code chunk not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            service = AIFeatureService()
            result = service.generate_tests(chunk_id, framework)
            return Response(
                {"status": "success", "data": AIFeatureResponseSerializer(result).data}
            )
        except Exception as e:
            logger.error(f"Generate tests failed: {e}")
            return Response(
                {"status": "error", "message": "Failed to generate tests."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DetectBugsView(BaseAIFeatureView):
    """
    POST /api/v1/ai/detect-bugs/

    Analyze code for potential bugs and issues.
    """

    def post(self, request):
        serializer = DetectBugsRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        chunk_id = str(serializer.validated_data["chunk_id"])

        chunk = self._validate_chunk_access(request, chunk_id)
        if not chunk:
            return Response(
                {"status": "error", "message": "Code chunk not found or access denied."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            service = AIFeatureService()
            result = service.detect_bugs(chunk_id)
            return Response(
                {"status": "success", "data": AIFeatureResponseSerializer(result).data}
            )
        except Exception as e:
            logger.error(f"Detect bugs failed: {e}")
            return Response(
                {"status": "error", "message": "Failed to analyze code."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
