from rest_framework import serializers

from apps.shops.models import Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'address', 'average_rating']
        read_only_fields = ['average_rating']
