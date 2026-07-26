"""
Common views — health checks and system status.
"""

from django.db import connection
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    GET /api/v1/health/

    System health check for monitoring and load balancers.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        health = {"status": "healthy", "checks": {}}

        # Database check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            health["checks"]["database"] = "ok"
        except Exception:
            health["checks"]["database"] = "error"
            health["status"] = "unhealthy"

        # Redis check
        try:
            from django.core.cache import cache
            cache.set("health_check", "ok", 5)
            if cache.get("health_check") == "ok":
                health["checks"]["cache"] = "ok"
            else:
                health["checks"]["cache"] = "error"
        except Exception:
            health["checks"]["cache"] = "unavailable"

        status_code = 200 if health["status"] == "healthy" else 503
        return Response(health, status=status_code)
