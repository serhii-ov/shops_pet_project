from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='category.name',
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'image',
            'category',
            'category_name',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'slug',
            'created_at',
            'updated_at',
        ]
