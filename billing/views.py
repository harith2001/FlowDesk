from decimal import Decimal

from rest_framework import permissions, viewsets

from organizations.permissions import IsOrganizationMember
from audit.mixins import AuditLogMixin

from .models import Invoice, InvoiceItem
from .serializers import InvoiceItemSerializer, InvoiceSerializer
from .tasks import generate_invoice_pdf


class InvoiceViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    Manage invoices for the current organization.
    """

    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        org = getattr(self.request, "organization", None)
        return Invoice.objects.filter(organization=org).prefetch_related("items")

    def perform_create(self, serializer):
        org = getattr(self.request, "organization", None)

        # Auto-generate invoice number: simple incremental per organization.
        last_invoice = (
            Invoice.objects.filter(organization=org)
            .order_by("-created_at")
            .first()
        )
        if last_invoice:
            try:
                last_number_int = int(last_invoice.number)
            except ValueError:
                last_number_int = 0
            next_number = f"{last_number_int + 1:05d}"
        else:
            next_number = "00001"

        invoice = serializer.save(
            organization=org,
            number=next_number,
            total_amount=Decimal("0.00"),
        )

        # Trigger PDF generation in background.
        generate_invoice_pdf.delay(invoice.id)


class InvoiceItemViewSet(AuditLogMixin, viewsets.ModelViewSet):
    """
    Manage invoice line items.
    """

    serializer_class = InvoiceItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrganizationMember]

    def get_queryset(self):
        org = getattr(self.request, "organization", None)
        return InvoiceItem.objects.filter(invoice__organization=org).select_related(
            "invoice"
        )

    def perform_create(self, serializer):
        item = serializer.save()
        self._recalculate_total(item.invoice)
        # Audit logging handled by AuditLogMixin
        super().perform_create(serializer)

    def perform_update(self, serializer):
        item = serializer.save()  # Save first
        super().perform_update(serializer)  # Logs (detects instance already saved)
        self._recalculate_total(item.invoice)

    def perform_destroy(self, instance):
        invoice = instance.invoice
        super().perform_destroy(instance)  # This logs and deletes
        self._recalculate_total(invoice)

    def _recalculate_total(self, invoice: Invoice) -> None:
        total = sum((item.line_total for item in invoice.items.all()), Decimal("0.00"))
        invoice.total_amount = total
        invoice.save(update_fields=["total_amount"])

