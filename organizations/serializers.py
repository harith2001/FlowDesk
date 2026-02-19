from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Organization, Membership


User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "slug", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class MembershipSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Membership
        fields = ["id", "user", "organization", "role", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

