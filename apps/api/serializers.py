"""DRF serializers for the API app."""

from __future__ import annotations


from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    """Serializer for the User model — read-only profile fields."""

    class Meta:
        model = UserModel
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = fields


class UserProfileUpdateSerializer(serializers.ModelSerializer):  # type: ignore[type-arg]
    """Serializer for updating user profile — only editable fields."""

    class Meta:
        model = UserModel
        fields = [
            "first_name",
            "last_name",
        ]
