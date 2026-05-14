from rest_framework import serializers

from apps.shop_products.models import ShopProduct


class ShopProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(
        source='shop.name',
        read_only=True
    )

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    class Meta:
        model = ShopProduct
        fields = [
            'id',
            'shop',
            'shop_name',
            'product',
            'product_name',
            'price',
            'stock',
            'is_available',
        ]

    def validate(self, attrs):
        shop = attrs.get('shop')
        product = attrs.get('product')

        queryset = ShopProduct.objects.filter(
            shop=shop,
            product=product
        )

        # exclude current instance during update
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)

        if queryset.exists():
            raise serializers.ValidationError(
                'This product already exists in this shop.'
            )

        return attrs
