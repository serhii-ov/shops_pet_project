from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

from apps.shop_products.models import ShopProduct
from apps.shop_products.serializers import ShopProductSerializer
from apps.users.permissions import IsAdmin


class ShopProductViewSet(viewsets.ModelViewSet):
    queryset = ShopProduct.objects.select_related(
        'shop',
        'product'
    ).order_by('id')

    serializer_class = ShopProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['shop', 'product', 'is_available']
    search_fields = ['product__name', 'shop__name']

    ordering_fields = [
        'id',
        'price',
        'stock',
        'product__name',
    ]

    def get_permissions(self):
        """
        Anyone can read.
        Only admins can create/update/delete.
        """

        if self.action in [
            'create',
            'update',
            'partial_update',
            'destroy'
        ]:
            return [IsAdmin()]

        return [AllowAny()]
