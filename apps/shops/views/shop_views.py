from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (
    AllowAny,
    )

from apps.shops.filters import ShopRatingFilter
from apps.users.permissions import (
    IsAdmin,
    )
from apps.shops.models import Shop

from apps.shops.serializers import (
    ShopSerializer, 
    )


class ShopListCreateView(generics.ListCreateAPIView):

    queryset = Shop.objects.all().order_by('-average_rating')
    serializer_class = ShopSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_class = ShopRatingFilter

    search_fields = ['name']
    ordering_fields = ['average_rating', 'name']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [AllowAny()]


class ShopRetrieveUpdateDestroyView(
    generics.RetrieveUpdateDestroyAPIView
    ):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin()]
        return [AllowAny()]
