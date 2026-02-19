from rest_framework import permissions, viewsets

from organizations.permissions import IsOrganizationMember
from audit.mixins import AuditLogMixin

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    CRUD for projects within the current organization.
    """

    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        org = getattr(self.request, "organization", None)
        return Project.objects.filter(organization=org)

    def perform_create(self, serializer):
        org = getattr(self.request, "organization", None)
        serializer.save(
            organization=org,
            owner=self.request.user if not serializer.validated_data.get("owner") else serializer.validated_data["owner"],
        )
        # Audit logging handled by AuditLogMixin
        super().perform_create(serializer)

