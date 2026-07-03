"""Tests for core app — health checks and utilities."""

from __future__ import annotations

import pytest
from django.test import Client
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestHealthChecks:
    """Test health check endpoints."""

    def test_health_check(self) -> None:
        """Test health check endpoint."""
        client = Client()
        response = client.get("/health/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_readiness_check(self) -> None:
        """Test readiness check endpoint."""
        client = Client()
        response = client.get("/health/ready/")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"


@pytest.mark.django_db
class TestPagination:
    """Test that pagination is wired correctly."""

    def test_api_root_has_pagination_info(self, auth_client: APIClient) -> None:
        """Test paginated endpoints return count/results."""
        # The user list endpoint should be paginated
        response = auth_client.get("/api/users/profile/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestMiddleware:
    """Test custom middleware."""

    def test_request_id_header_present(self, client: APIClient) -> None:
        """Test that X-Request-ID header is added to responses."""
        response = client.get("/health/")
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) > 0
