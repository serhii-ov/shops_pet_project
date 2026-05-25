from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.carts.mixins import CartMixin
from apps.carts.models.cart_item_model import CartItem
from apps.carts.serializers import (
    CartSerializer,
    CartItemSerializer,
)
from apps.carts.services import CartService
from apps.carts.permissions import IsCartOwner
from apps.shops.models import Shop


class AddCartItemView(
    CartMixin,
    generics.CreateAPIView,
):

    serializer_class = CartItemSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):

        shop = generics.get_object_or_404(
            Shop,
            id=self.kwargs['shop_id'],
        )

        cart = self.get_cart(shop)

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        CartService.add_item(
            cart=cart,
            shop_product=serializer.validated_data[
                'shop_product'
            ],
            quantity=serializer.validated_data[
                'quantity'
            ],
        )

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_201_CREATED,
        )
    

class CartItemUpdateView(
    generics.UpdateAPIView,
):

    serializer_class = CartItemSerializer
    permission_classes = [
        permissions.AllowAny,
        IsCartOwner,
    ]

    queryset = CartItem.objects.select_related(
        'shop_product',
        'shop_product__shop',
        'shop_product__product',
        'cart',
    )

    http_method_names = ['patch']

    def perform_update(self, serializer):

        CartService.update_item_quantity(
            cart_item=self.get_object(),
            quantity=serializer.validated_data[
                'quantity'
            ],
        )


class CartItemDeleteView(
    CartMixin,
    generics.DestroyAPIView, 
):

    permission_classes = [
        permissions.AllowAny,
        IsCartOwner,
    ]

    queryset = CartItem.objects.all()

    def perform_destroy(self, instance):

        CartService.remove_item(
            cart_item=instance,
        )
