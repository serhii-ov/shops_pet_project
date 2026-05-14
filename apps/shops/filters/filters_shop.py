from django_filters import rest_framework as filters

from apps.shops.models import Shop


class ShopRatingFilter(filters.FilterSet):

    class Meta:
        model = Shop
        fields = {
            'average_rating': [
                'exact',
                'gte',
                'lte',
                'gt',
                'lt',
            ]
        }
