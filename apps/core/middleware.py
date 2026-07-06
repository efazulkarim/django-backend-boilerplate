"""Custom middleware for request logging and tracing."""

from __future__ import annotations

import logging
import uuid
from typing import Callable

from django.http import HttpRequest, HttpResponse
from apps.core.logging import request_id_var

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:  # pylint: disable=too-few-public-methods
    """Attach a request ID and log request/response cycle.

    Adds X-Request-ID header to every response for trace correlation.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = (
            request.headers.get("X-Request-ID")
            or request.META.get("HTTP_X_REQUEST_ID")
            or str(uuid.uuid4())
        )
        request.request_id = request_id  # type: ignore[attr-defined]

        # Bind request_id to context variable
        token = request_id_var.set(request_id)
        try:
            logger.info(
                "request_started",
                extra={
                    "method": request.method,
                    "path": request.path,
                },
            )

            response = self.get_response(request)

            # Log user ID if authenticated (now available after view/auth middleware has executed)
            user_id = None
            if hasattr(request, "user") and request.user.is_authenticated:
                user_id = request.user.id

            logger.info(
                "request_completed",
                extra={
                    "status_code": response.status_code,
                    "user_id": user_id,
                },
            )

            response["X-Request-ID"] = request_id
            return response
        finally:
            # Clean up context
            request_id_var.reset(token)
