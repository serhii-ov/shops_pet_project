from rest_framework import serializers

from apps.orders.models import Order
from .order_item_serializer import (
    OrderItemSerializer,
)


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )
    total_items = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "shop",

            "status",

            "payment_status",
            "payment_provider_id",

            "shipment_status",
            "delivery_notes",

            "cancellation_reason",

            "customer_name",
            "customer_email",
            "customer_phone",
            "customer_address",

            "items",
            "total_price",
            "total_items",

            "paid_at",
            "shipped_at",
            "completed_at",

            "created_at",
        ]

        read_only_fields = [
            "status",
            "payment_status",
            "shipment_status",

            "payment_provider_id",

            "items",
            "total_price",
            "total_items",

            "paid_at",
            "shipped_at",
            "completed_at",

            "created_at",
        ]
