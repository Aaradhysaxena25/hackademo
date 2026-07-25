"""
Custom pagination classes for CodePilot API.
"""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for API endpoints."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """Larger pagination for endpoints that need more results."""

    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200
