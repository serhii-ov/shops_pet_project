from rest_framework import serializers

from apps.orders.models import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "shop_product",
            "product_name",
            "price",
            "quantity",
            "total_price",
        ]
        read_only_fields = [
            "id",
            "product_name",
            "price",
            "total_price",
        ]
