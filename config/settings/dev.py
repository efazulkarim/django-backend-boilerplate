# pylint: disable=wildcard-import,unused-wildcard-import
"""Development settings."""

from .base import *  # noqa: F403

# Override for development
DEBUG = True
ALLOWED_HOSTS = [
    "*",
]

# Email backend (for testing with Mailpit)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@example.com"

# CORS for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
