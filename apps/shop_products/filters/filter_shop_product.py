from django_filters import rest_framework as filters

from apps.shops.models import ShopProduct


class ShopProductFilter(filters.FilterSet):

    category = filters.NumberFilter(
        field_name='product__category__id'
    )

    category_name = filters.CharFilter(
        field_name='product__category__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = ShopProduct
        fields = [
            'category',
            'category_name',
            'is_available',
        ]
