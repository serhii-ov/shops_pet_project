from rest_framework import serializers

from .cart_item_serializer import (
    CartItemSerializer,
    )
from apps.carts.models import Cart


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'shop',
            'items',
            'total_price',
            'total_items',
            'is_active',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'user',
            'total_price',
            'total_items',
            'created_at',
            'updated_at',
        ]
