"""Reusable DRF permission classes."""

from __future__ import annotations

from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwner(BasePermission):
    """Allow access only to the object's owner.

    Expects the view's object to have a `user` or `author` attribute
    that matches request.user.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        owner = getattr(obj, "user", None) or getattr(obj, "author", None)
        if owner is None:
            return False
        return bool(owner == request.user)


class IsAdmin(BasePermission):
    """Allow access only to admin/staff users."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(BasePermission):
    """Allow write access only to the owner; read access to all."""

    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "author", None)
        if owner is None:
            return False
        return bool(owner == request.user)
