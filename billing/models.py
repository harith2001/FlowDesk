from decimal import Decimal

from django.db import models

from core.models import OrganizationScopedModel, TimeStampedModel


class Invoice(OrganizationScopedModel):
    STATUS_DRAFT = "draft"
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_OVERDUE = "overdue"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_OVERDUE, "Overdue"),
    ]

    number = models.CharField(max_length=50)
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    pdf_file = models.FileField(
        upload_to="invoices/",
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ("organization", "number")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Invoice {self.number}"


class InvoiceItem(TimeStampedModel):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items",
    )
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self) -> Decimal:
        return self.quantity * self.unit_price

