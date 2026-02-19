from rest_framework import serializers

from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user",
            "organization",
            "action",
            "model_name",
            "object_id",
            "before",
            "after",
            "created_at",
        ]
        read_only_fields = fields

