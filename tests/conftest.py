"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import os
import sys
from typing import Any

import django
import pytest
from rest_framework.test import APIClient

from tests.factories import UserFactory


def pytest_configure() -> None:
    """Configure Django settings for pytest."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.test")
    sys.path.insert(0, os.path.dirname(__file__))
    django.setup()


@pytest.fixture
def user(db: None) -> Any:
    """Create a standard user."""
    return UserFactory()  # type: ignore[no-untyped-call]


@pytest.fixture
def admin_user(db: None) -> Any:
    """Create an admin/staff user."""
    return UserFactory(is_staff=True)  # type: ignore[no-untyped-call]


@pytest.fixture
def client() -> APIClient:
    """DRF API client (unauthenticated)."""
    return APIClient()


@pytest.fixture
def auth_client(user: Any) -> APIClient:
    """DRF API client authenticated as a standard user."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def admin_client(admin_user: Any) -> APIClient:
    """DRF API client authenticated as an admin."""
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client
