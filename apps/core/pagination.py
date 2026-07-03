"""Custom pagination classes."""

from __future__ import annotations

from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """Default pagination: page-number style with configurable page size.

    Usage:
        GET /api/resource/?page=2&page_size=10
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: list[Any]) -> Response:
        assert self.page is not None
        assert self.request is not None
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "page_size": self.get_page_size(self.request),
                "results": data,
            }
        )
