from rest_framework import serializers

from apps.carts.serializers.cart_item_serializer import (
    CartItemSerializer,
    )
from apps.carts.models import Cart


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'items',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'user',
            'created_at',
            'updated_at',
        ]
