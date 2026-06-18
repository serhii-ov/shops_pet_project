from rest_framework import serializers

from apps.orders.models import Order

from .order_item_serializer import (
    OrderItemSerializer,
)


class OrderDetailSerializer(
    serializers.ModelSerializer
):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order

        fields = (
            "id",
            "order_number",
            "status",
            "payment_status",
            "shipment_status",
            "payment_method",
            "customer_name",
            "customer_email",
            "customer_phone",
            "customer_address",
            "delivery_notes",
            "tracking_number",
            "total_price",
            "shipping_cost",
            "tax_amount",
            "discount_amount",
            "total",
            "total_items",
            "paid_at",
            "shipped_at",
            "completed_at",
            "cancelled_at",
            "created_at",
            "updated_at",
            "items",
        )