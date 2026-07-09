"""Celery configuration."""

import os
import threading
from typing import Any
from celery import Celery  # pylint: disable=import-self
from celery.signals import before_task_publish, task_prerun, task_postrun

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("my_api_project")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(
    [
        "apps",
        "config",
    ]
)


# Thread-local registry to securely hold request tokens per task ID, preventing concurrency race conditions
_local_tokens = threading.local()


def _get_token_registry() -> dict[str, Any]:
    """Retrieve or initialize the thread-local token registry."""
    if not hasattr(_local_tokens, "registry"):
        _local_tokens.registry = {}
    return _local_tokens.registry  # type: ignore[no-any-return]


# Trace Correlation ID Propagation Signals
@before_task_publish.connect  # type: ignore[untyped-decorator]
def before_task_publish_handler(
    headers: dict[str, str] | None = None, body: Any = None, **kwargs: Any
) -> None:
    """Propagate the current request's correlation ID to the Celery task context."""
    from apps.core.logging import request_id_var

    if headers is not None:
        headers["x_request_id"] = request_id_var.get()


@task_prerun.connect  # type: ignore[untyped-decorator]
def task_prerun_handler(task: Any, **kwargs: Any) -> None:
    """Restore the correlation ID from the task headers into the local logging context."""
    from apps.core.logging import request_id_var

    request_id = None
    task_id = "unknown"

    request = getattr(task, "request", None)
    if request is not None:
        headers = request.headers or {}
        request_id = headers.get("x_request_id")
        task_id = getattr(request, "id", "unknown")
        if not request_id and task_id != "unknown":
            request_id = f"task-{task_id}"

    if not request_id:
        request_id = f"task-{task_id}"

    token = request_id_var.set(request_id)
    if request is not None and task_id != "unknown":
        registry = _get_token_registry()
        registry[task_id] = token


@task_postrun.connect  # type: ignore[untyped-decorator]
def task_postrun_handler(task: Any, **kwargs: Any) -> None:
    """Clean up the logging context after task execution finishes."""
    from apps.core.logging import request_id_var

    request = getattr(task, "request", None)
    if request is not None:
        task_id = getattr(request, "id", "unknown")
        if task_id != "unknown":
            registry = _get_token_registry()
            token = registry.pop(task_id, None)
            if token is not None:
                request_id_var.reset(token)
