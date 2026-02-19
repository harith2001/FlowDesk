from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OrganizationScopedModel(TimeStampedModel):
    """
    Abstract base for models that belong to an organization.
    """

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="%(class)ss",
    )

    class Meta:
        abstract = True

