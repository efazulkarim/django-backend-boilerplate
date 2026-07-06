# pylint: disable=wildcard-import,unused-wildcard-import
"""Production settings."""

import os

from .base import *  # noqa: F403

# Override for production
DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Email configuration (configure for production)
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@example.com")

# Media storage (S3 for production)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "us-east-1")

# Production database
DATABASES["default"].update(  # noqa: F405
    {
        "ENGINE": "django_prometheus.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME") or "",
        "USER": os.environ.get("DB_USER") or "",
        "PASSWORD": os.environ.get("DB_PASSWORD") or "",
        "HOST": os.environ.get("DB_HOST") or "",
        "PORT": os.environ.get("DB_PORT") or "",
    }
)

# Production Redis Cache overrides (updating location and merging options selectively)
CACHES["default"]["LOCATION"] = os.environ.get("REDIS_URL", "redis://redis:6379/1")  # noqa: F405
options = CACHES["default"].setdefault("OPTIONS", {})  # noqa: F405
if isinstance(options, dict):
    options.update(
        {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": int(os.environ.get("REDIS_MAX_CONNECTIONS", 100)),
                "retry_on_timeout": True,
            },
        }
    )
