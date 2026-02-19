from django.conf import settings
from django.db import models

from core.models import TimeStampedModel


class Notification(TimeStampedModel):
    """
    Simple notification model to back real-time and historical notifications.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    type = models.CharField(max_length=100)
    payload = models.JSONField(default=dict, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

