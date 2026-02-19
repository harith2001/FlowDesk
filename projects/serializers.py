from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project


User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Project
        fields = [
            "id",
            "organization",
            "name",
            "description",
            "owner",
            "status",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "organization", "created_at", "updated_at"]

