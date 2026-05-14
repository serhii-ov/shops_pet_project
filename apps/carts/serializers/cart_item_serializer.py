from rest_framework import serializers

from apps.carts.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='shop_product.product.name',
        read_only=True,
    )

    shop_name = serializers.CharField(
        source='shop_product.shop.name',
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'shop_product',
            'product_name',
            'shop_name',
            'quantity',
        ]

    def validate(self, attrs):
        shop_product = attrs['shop_product']
        quantity = attrs['quantity']

        if not shop_product.is_available:
            raise serializers.ValidationError(
                'Product is not available.'
            )

        if quantity > shop_product.stock:
            raise serializers.ValidationError(
                'Not enough stock available.'
            )

        return attrs
