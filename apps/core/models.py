"""Abstract base models for reuse across all apps."""

from __future__ import annotations


from django.db import models


class TimestampedModel(models.Model):
    """Abstract base model with created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SoftDeleteManager(models.Manager["SoftDeleteModel"]):  # pylint: disable=too-few-public-methods
    """Manager that excludes soft-deleted objects by default."""

    def get_queryset(self) -> models.QuerySet[SoftDeleteModel]:
        """Exclude soft-deleted items from query results."""
        return super().get_queryset().filter(is_deleted=False)


class SoftDeleteModel(TimestampedModel):
    """Abstract base model with soft delete support.

    Use .delete() to soft-delete (sets is_deleted=True, preserves row).
    Use .hard_delete() to permanently remove.
    Use .all_objects to include soft-deleted rows.
    """

    is_deleted = models.BooleanField(default=False, db_index=True)

    objects: SoftDeleteManager = SoftDeleteManager()
    all_objects: models.Manager[SoftDeleteModel] = models.Manager()

    class Meta:
        abstract = True

    def delete(
        self, using: str | None = None, keep_parents: bool = False
    ) -> tuple[int, dict[str, int]]:
        """Soft-delete: mark as deleted, don't remove row."""
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])
        return (0, {})

    def hard_delete(
        self, using: str | None = None, keep_parents: bool = False
    ) -> tuple[int, dict[str, int]]:
        """Permanently remove the row from the database."""
        return super().delete(using=using, keep_parents=keep_parents)

    def restore(self) -> None:
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.save(update_fields=["is_deleted", "updated_at"])
