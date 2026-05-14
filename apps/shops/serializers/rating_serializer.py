from rest_framework import serializers

from apps.shops.models import ShopRating


class ShopRatingSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    shop_name = serializers.CharField(
        source="shop.name",
        read_only=True
    )

    class Meta:
        model = ShopRating
        fields = [
            "id",
            "shop",
            "shop_name",
            "customer",
            "rating",
            "created_at",
        ]
        read_only_fields = ["customer", "created_at"]
