from rest_framework import permissions, viewsets

from organizations.permissions import IsOrganizationMember
from audit.mixins import AuditLogMixin

from .models import Task, TaskComment
from .serializers import TaskCommentSerializer, TaskSerializer


class TaskViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    CRUD for tasks scoped to the current organization.
    """

    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        org = getattr(self.request, "organization", None)
        return Task.objects.filter(organization=org).select_related("project", "assignee")

    def perform_create(self, serializer):
        org = getattr(self.request, "organization", None)
        serializer.save(organization=org)
        # Audit logging handled by AuditLogMixin
        super().perform_create(serializer)


class TaskCommentViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    Manage comments on tasks within the current organization.
    """

    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        org = getattr(self.request, "organization", None)
        return TaskComment.objects.filter(task__organization=org).select_related(
            "task", "author"
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        # Audit logging handled by AuditLogMixin
        super().perform_create(serializer)

