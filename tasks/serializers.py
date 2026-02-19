from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Task, TaskComment


User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "organization",
            "project",
            "title",
            "description",
            "status",
            "assignee",
            "due_date",
            "priority",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "organization", "created_at", "updated_at"]


class TaskCommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TaskComment
        fields = [
            "id",
            "task",
            "author",
            "body",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "author", "created_at", "updated_at"]

