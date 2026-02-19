from __future__ import annotations

from typing import Any, Dict, Optional

from django.db import models

from .models import AuditLog


class AuditLogMixin:
    """
    Reusable mixin for DRF viewsets to automatically log create/update/delete.
    """

    audit_log_model = AuditLog

    def _get_organization_for_instance(self, instance: models.Model):
        # Direct organization attribute
        org = getattr(instance, "organization", None)
        if org is not None:
            return org

        # Common indirections
        for attr in ["project", "invoice", "task"]:
            parent = getattr(instance, attr, None)
            if parent is not None:
                org = getattr(parent, "organization", None)
                if org is not None:
                    return org

        # Fallback to request.organization if available
        request = getattr(self, "request", None)
        return getattr(request, "organization", None) if request else None

    def _serialize_instance(self, instance: Optional[models.Model]) -> Optional[Dict[str, Any]]:
        if instance is None:
            return None
        data: Dict[str, Any] = {}
        for field in instance._meta.fields:
            name = field.name
            value = getattr(instance, name)
            # Represent related fields by their primary key
            if isinstance(field, (models.ForeignKey, models.OneToOneField)):
                value = getattr(value, "pk", None)
            data[name] = value
        return data

    def _create_audit_log(
        self,
        *,
        instance: models.Model,
        action: str,
        before: Optional[Dict[str, Any]],
        after: Optional[Dict[str, Any]],
    ) -> None:
        AuditLogModel = self.audit_log_model
        AuditLogModel.objects.create(
            user=getattr(self.request, "user", None),
            organization=self._get_organization_for_instance(instance),
            action=action,
            model_name=instance._meta.label,
            object_id=str(getattr(instance, "pk", "")),
            before=before,
            after=after,
        )

    # Hooks

    def perform_create(self, serializer):
        # Check if instance was already saved (by subclass override)
        if serializer.instance and serializer.instance.pk:
            instance = serializer.instance
        else:
            instance = serializer.save()
        self._create_audit_log(
            instance=instance,
            action=AuditLog.ACTION_CREATE,
            before=None,
            after=self._serialize_instance(instance),
        )

    def perform_update(self, serializer):
        instance = self.get_object()
        before = self._serialize_instance(instance)
        # Check if instance was already saved (by subclass override)
        if serializer.instance and serializer.instance.pk:
            instance = serializer.instance
        else:
            instance = serializer.save()
        self._create_audit_log(
            instance=instance,
            action=AuditLog.ACTION_UPDATE,
            before=before,
            after=self._serialize_instance(instance),
        )

    def perform_destroy(self, instance):
        before = self._serialize_instance(instance)
        self._create_audit_log(
            instance=instance,
            action=AuditLog.ACTION_DELETE,
            before=before,
            after=None,
        )
        super().perform_destroy(instance)

