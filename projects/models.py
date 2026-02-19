from django.conf import settings
from django.db import models

from core.models import OrganizationScopedModel


class Project(OrganizationScopedModel):
    STATUS_PLANNED = "planned"
    STATUS_ACTIVE = "active"
    STATUS_ON_HOLD = "on_hold"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = [
        (STATUS_PLANNED, "Planned"),
        (STATUS_ACTIVE, "Active"),
        (STATUS_ON_HOLD, "On hold"),
        (STATUS_COMPLETED, "Completed"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_projects",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PLANNED,
    )
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name

