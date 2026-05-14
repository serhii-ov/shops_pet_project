from rest_framework import serializers

from apps.orders.models.order_item_model import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'shop_product',
            'quantity',
            'price',
        ]
        read_only_fields = [
            'price',
        ]
