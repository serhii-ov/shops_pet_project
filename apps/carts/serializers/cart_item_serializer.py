from rest_framework import serializers

from apps.carts.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):

    shop_name = serializers.CharField(
        source='shop_product.shop.name',
        read_only=True,
    )

    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'shop_product',
            'product_name',
            'shop_name',
            'price',
            'quantity',
            'total_price',
        ]

        read_only_fields = [
            'product_name',
            'price',
            'total_price',
        ]

    def validate(self, attrs):
        shop_product = attrs.get(
            'shop_product',
            getattr(self.instance, 'shop_product', None)
        )

        quantity = attrs.get(
            'quantity',
            getattr(self.instance, 'quantity', None)
        )

        if shop_product and not shop_product.is_available:
            raise serializers.ValidationError(
                'Product is not available.'
            )

        if (
            shop_product and
            quantity and
            quantity > shop_product.stock
        ):
            raise serializers.ValidationError(
                'Not enough stock available.'
            )

        return attrs
