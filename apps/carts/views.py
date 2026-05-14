from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
)


class CartViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(
            user=self.request.user
        ).prefetch_related(
            'items',
            'items__shop_product',
            'items__shop_product__product',
            'items__shop_product__shop',
        )


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user
        ).select_related(
            'shop_product',
            'shop_product__product',
            'shop_product__shop',
        )

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(
            user=self.request.user
        )

        serializer.save(cart=cart)
