"""Test factories using factory_boy.

Usage in tests:
    user = UserFactory()
    admin = UserFactory(is_staff=True)
    users = UserFactory.create_batch(10)
"""

from __future__ import annotations

from typing import Any

import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):  # type: ignore[type-arg]
    """Factory for the custom User model."""

    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")  # type: ignore[attr-defined,no-untyped-call]
    first_name = factory.Faker("first_name")  # type: ignore[attr-defined,no-untyped-call]
    last_name = factory.Faker("last_name")  # type: ignore[attr-defined,no-untyped-call]
    is_active = True
    is_staff = False

    @factory.post_generation  # type: ignore[attr-defined,untyped-decorator]
    def password(self, create: bool, extracted: str | None, **kwargs: Any) -> None:
        """Set password after user creation."""
        password = extracted or "testpass123"
        self.set_password(password)  # type: ignore[attr-defined]
        if create:
            self.save()  # type: ignore[attr-defined]
