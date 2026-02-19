from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model.

    Users can belong to multiple organizations via organizations.Membership.
    """

    full_name = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.get_full_name() or self.username

