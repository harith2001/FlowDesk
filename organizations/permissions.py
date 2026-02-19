from django.contrib.auth import get_user_model
from rest_framework import permissions

from .models import Membership


User = get_user_model()


class IsOrganizationMember(permissions.BasePermission):
    """
    Allows access only to users that are members of the current organization.
    """

    def has_permission(self, request, view) -> bool:
        org = getattr(request, "organization", None)
        user = request.user
        if not org or not user.is_authenticated:
            return False
        return Membership.objects.filter(user=user, organization=org).exists()


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows access only to organization owners or admins.
    """

    def has_permission(self, request, view) -> bool:
        org = getattr(request, "organization", None)
        user = request.user
        if not org or not user.is_authenticated:
            return False

        return Membership.objects.filter(
            user=user,
            organization=org,
            role__in=[Membership.OWNER, Membership.ADMIN],
        ).exists()

