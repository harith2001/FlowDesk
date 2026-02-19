from rest_framework import permissions, viewsets

from organizations.permissions import IsOrganizationMember, IsOwnerOrAdmin

from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only access to audit logs for the current organization.
    Restricted to organization owners/admins.
    """

    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember, IsOwnerOrAdmin]

    def get_queryset(self):
        org = getattr(self.request, "organization", None)
        return AuditLog.objects.filter(organization=org)

