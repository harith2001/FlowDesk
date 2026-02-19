from __future__ import annotations

from celery import shared_task

from .models import Invoice


@shared_task
def generate_invoice_pdf(invoice_id: int) -> None:
    """
    Background task to generate a PDF for an invoice.

    For now this is a stub that simply marks the invoice as having a PDF.
    In a real implementation you would render a template to PDF here.
    """

    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:  # pragma: no cover - defensive
        return

    # Stub implementation: just pretend a PDF was generated.
    if not invoice.pdf_file:
        invoice.pdf_file.name = f"invoices/{invoice.number}.pdf"
        invoice.save(update_fields=["pdf_file"])

