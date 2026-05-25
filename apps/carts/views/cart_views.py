from rest_framework import generics, permissions

from apps.carts.mixins import CartMixin
from apps.carts.permissions import IsCartOwner
from apps.carts.selectors.cart_selectors import (
    get_cart_with_items,
)
from apps.carts.serializers import CartSerializer
from apps.shops.models import Shop


class CartDetailView(
    CartMixin,
    generics.RetrieveAPIView,
):

    serializer_class = CartSerializer

    permission_classes = [
        permissions.AllowAny,
        IsCartOwner,
    ]

    def get_object(self):

        shop = generics.get_object_or_404(
            Shop,
            id=self.kwargs['shop_id'],
        )

        cart = self.get_cart(shop)

        return get_cart_with_items(cart.id)
