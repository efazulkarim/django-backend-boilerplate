"""Users admin configuration."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User

if TYPE_CHECKING:
    _BaseUserAdmin = BaseUserAdmin[User]
else:
    _BaseUserAdmin = BaseUserAdmin


class UserAdmin(_BaseUserAdmin):
    """Custom user admin."""

    ordering = ("email",)
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ((None, {"fields": ("email", "password1", "password2")}),)
    add_form = UserCreationForm
    form = UserChangeForm  # type: ignore[assignment]


admin.site.register(User, UserAdmin)
