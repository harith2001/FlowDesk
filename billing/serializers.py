from decimal import Decimal

from rest_framework import serializers

from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = [
            "id",
            "invoice",
            "description",
            "quantity",
            "unit_price",
            "line_total",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "line_total", "created_at", "updated_at"]

    def get_line_total(self, obj) -> Decimal:
        return obj.line_total


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "organization",
            "number",
            "client_name",
            "client_email",
            "issue_date",
            "due_date",
            "status",
            "total_amount",
            "pdf_file",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "organization", "total_amount", "pdf_file", "created_at", "updated_at"]

