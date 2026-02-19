from django.contrib.auth import get_user_model
from rest_framework import mixins, permissions, viewsets

from audit.mixins import AuditLogMixin
from .models import Organization, Membership
from .permissions import IsOwnerOrAdmin, IsOrganizationMember
from .serializers import MembershipSerializer, OrganizationSerializer


User = get_user_model()


class OrganizationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Manage organizations.

    - Anyone authenticated can list organizations they belong to.
    - Creating an organization also creates an OWNER membership for the creator.
    """

    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Organization.objects.filter(memberships__user=user).distinct()

    def perform_create(self, serializer):
        org = serializer.save()
        Membership.objects.create(
            user=self.request.user,
            organization=org,
            role=Membership.OWNER,
        )


class MembershipViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Manage organization memberships.

    Restricted to owner/admins of the current organization.
    """

    serializer_class = MembershipSerializer
    permission_classes = [IsOwnerOrAdmin & IsOrganizationMember]

    def get_queryset(self):
        org = getattr(self.request, "organization", None)
        return Membership.objects.filter(organization=org)

    def perform_create(self, serializer):
        org = getattr(self.request, "organization", None)
        serializer.save(organization=org)

