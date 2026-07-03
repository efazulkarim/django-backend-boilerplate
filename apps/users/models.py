"""User models with email-based authentication."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

if TYPE_CHECKING:
    pass


class UserManager(BaseUserManager["User"]):
    """Custom user manager that uses email instead of username."""

    def create_user(self, email: str, password: str | None = None, **extra_fields: object) -> User:
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: object
    ) -> User:
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model using email as username."""

    # Remove username field, use email instead
    username = None  # type: ignore[assignment]
    email = models.EmailField(unique=True, verbose_name="email address")

    objects: UserManager = UserManager()  # type: ignore[assignment,misc]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []  # type: ignore[misc]

    def __str__(self) -> str:
        return self.email
