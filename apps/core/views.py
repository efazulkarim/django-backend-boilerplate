import logging
from django.db import connections
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    """Detailed health check validating PostgreSQL, Redis Cache, and Celery Broker.

    If any component is unhealthy, returns HTTP 503 Service Unavailable.
    """
    from django.conf import settings

    health_status = "healthy"
    details = {}

    # 1. Check PostgreSQL Database
    try:
        db_conn = connections["default"]
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        details["database"] = {"status": "ok"}
    except Exception as e:
        health_status = "unhealthy"
        details["database"] = {"status": "error", "message": "Database connection failed"}
        logger.error(f"Health check failed: database connection error: {e}", exc_info=True)

    # 2. Check Redis Cache
    try:
        cache.set("health_check_ping", "pong", timeout=5)
        if cache.get("health_check_ping") == "pong":
            details["cache"] = {"status": "ok"}
        else:
            raise ValueError("Cache read/write verification mismatch")
    except Exception as e:
        health_status = "unhealthy"
        details["cache"] = {"status": "error", "message": "Cache connection failed"}
        logger.error(f"Health check failed: cache connection error: {e}", exc_info=True)

    # 3. Check Celery Broker Connection
    try:
        if getattr(settings, "CELERY_BROKER_URL", "").startswith("memory://") or getattr(
            settings, "CELERY_TASK_ALWAYS_EAGER", False
        ):
            # In testing/CI with memory settings, skip connection check
            details["broker"] = {"status": "ok", "message": "in-memory (eager)"}
        else:
            from config.celery import app as celery_app

            with celery_app.connection() as conn:
                conn.ensure_connection(max_retries=1)
            details["broker"] = {"status": "ok"}
    except Exception as e:
        health_status = "unhealthy"
        details["broker"] = {"status": "error", "message": "Celery broker connection failed"}
        logger.error(f"Health check failed: celery broker connection error: {e}", exc_info=True)

    # Choose HTTP status code: 200 if all is healthy, 503 otherwise
    http_status = (
        status.HTTP_200_OK if health_status == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    )

    return Response(
        {
            "status": health_status,
            "service": "my-api-project",
            "database": "connected"
            if details.get("database", {}).get("status") == "ok"
            else "disconnected",
            "details": details,
        },
        status=http_status,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def readiness_check(request: Request) -> Response:
    """Readiness check endpoint.

    Verifies database connectivity before declaring the app ready to receive traffic.
    """
    try:
        db_conn = connections["default"]
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        return Response(
            {
                "status": "ready",
                "service": "my-api-project",
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.error(f"Readiness check failed: system not ready: {e}", exc_info=True)
        return Response(
            {
                "status": "not_ready",
                "service": "my-api-project",
                "error": "Database connection failed",
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
