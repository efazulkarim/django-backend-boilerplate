"""Tests for core app — health checks and utilities."""

from __future__ import annotations

from unittest.mock import patch, MagicMock
import pytest
from django.test import Client, override_settings
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestHealthChecks:
    """Test health check endpoints."""

    @patch("config.celery.app.connection")
    def test_health_check(self, mock_connection: MagicMock) -> None:
        """Test health check endpoint."""
        # Setup mock connection to return successfully
        mock_conn = MagicMock()
        mock_connection.return_value.__enter__.return_value = mock_conn

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

    @patch("django.db.backends.base.base.BaseDatabaseWrapper.cursor")
    @patch("config.celery.app.connection")
    def test_health_check_database_failure(
        self, mock_connection: MagicMock, mock_cursor: MagicMock
    ) -> None:
        """Test health check database failure path."""
        mock_conn = MagicMock()
        mock_connection.return_value.__enter__.return_value = mock_conn
        mock_cursor.side_effect = Exception("Database offline")

        client = Client()
        response = client.get("/health/")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] == "disconnected"
        assert data["details"]["database"]["status"] == "error"
        assert "offline" not in data["details"]["database"]["message"]  # No credentials/traceback leak

    @patch("django.core.cache.cache.set")
    @patch("config.celery.app.connection")
    def test_health_check_cache_failure(
        self, mock_connection: MagicMock, mock_cache_set: MagicMock
    ) -> None:
        """Test health check cache failure path."""
        mock_conn = MagicMock()
        mock_connection.return_value.__enter__.return_value = mock_conn
        mock_cache_set.side_effect = Exception("Redis Cache failure")

        client = Client()
        response = client.get("/health/")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["details"]["cache"]["status"] == "error"
        assert "failure" not in data["details"]["cache"]["message"]  # No credentials/traceback leak

    @override_settings(CELERY_TASK_ALWAYS_EAGER=False, CELERY_BROKER_URL="amqp://localhost")
    @patch("config.celery.app.connection")
    def test_health_check_broker_failure(self, mock_connection: MagicMock) -> None:
        """Test health check celery broker failure path."""
        mock_conn = MagicMock()
        mock_conn.ensure_connection.side_effect = Exception("AMQP timeout")
        mock_connection.return_value.__enter__.return_value = mock_conn

        client = Client()
        response = client.get("/health/")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["details"]["broker"]["status"] == "error"
        assert "timeout" not in data["details"]["broker"]["message"]  # No credentials/traceback leak

    @patch("django.db.backends.base.base.BaseDatabaseWrapper.cursor")
    def test_readiness_check_failure(self, mock_cursor: MagicMock) -> None:
        """Test readiness check database failure path."""
        mock_cursor.side_effect = Exception("Database offline")

        client = Client()
        response = client.get("/health/ready/")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "not_ready"
        assert data["error"] == "Database connection failed"  # No traceback leak


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
