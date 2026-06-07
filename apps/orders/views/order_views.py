from rest_framework import generics, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apps.orders.selectors.order_selectors import (
    get_user_orders,
)
from apps.orders.serializers import OrderSerializer
from apps.orders.services import OrderService
from apps.carts.mixins import CartMixin
from apps.shops.models import Shop


class CreateOrderView(
        CartMixin,
        generics.CreateAPIView,
    ):

    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def create(self, request, *args, **kwargs):

        shop = generics.get_object_or_404(
            Shop,
            id=self.kwargs["shop_id"],
        )
        cart = self.get_cart(shop)
        order = OrderService.create_order_from_cart(
            cart=cart,
            customer_name=request.data[
                "customer_name"
            ],
            customer_email=request.data[
                "customer_email"
            ],
            customer_phone=request.data[
                "customer_phone"
            ],
            customer_address=request.data[
                "customer_address"
            ],
        )

        serializer = self.get_serializer(order)

        return Response(serializer.data)


class OrderDetailView(
    generics.RetrieveAPIView,
):
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    lookup_field = "id"

    def get_object(self):

        order = get_object_or_404(
            get_user_orders(self.request.user),
            id=self.kwargs["id"],
        )

        self.check_object_permissions(
            self.request,
            order,
        )

        return order
    

class UserOrdersListView(
    generics.ListAPIView,
):
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):

        return get_user_orders(
            self.request.user
        )
    