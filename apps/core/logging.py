"""Logging utilities for request correlation tracing."""

from __future__ import annotations

import contextvars
import logging

# Context variable to hold the request ID for the current thread/task
request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")


class RequestIDFilter(logging.Filter):
    """Logging filter to inject request_id into all log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get()
        return True
