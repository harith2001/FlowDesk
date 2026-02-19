from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Organization(TimeStampedModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Membership(TimeStampedModel):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"

    ROLE_CHOICES = [
        (OWNER, "Owner"),
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
        (EMPLOYEE, "Employee"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ("user", "organization")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.user} in {self.organization} ({self.role})"

