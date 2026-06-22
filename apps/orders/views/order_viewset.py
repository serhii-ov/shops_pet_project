from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.orders.models import Order
from apps.orders.serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    OrderStatusUpdateSerializer,
)
from apps.orders.services.order_service import (
    OrderService,
)
from apps.orders.services.order_status_service import (
    OrderStatusService,
)
from apps.carts.models import Cart


class OrderViewSet(ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .select_related("shop")
            .prefetch_related("items")
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderDetailSerializer

    @action(
        detail=False,
        methods=["post"],
        url_path="create-from-cart",
    )
    def create_from_cart(self, request):

        serializer = OrderCreateSerializer(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        cart = Cart.objects.get(
            user=request.user,
            is_active=True,
        )

        order = (
            OrderService.create_order_from_cart(
                cart=cart,
                **serializer.validated_data,
            )
        )

        return Response(
            OrderDetailSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )
    
    @action(
        detail=True,
        methods=["post"],
        url_path="status",
    )
    def update_status(self, request, pk=None):

        order = self.get_object()

        serializer = (
            OrderStatusUpdateSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        status_value = (
            serializer.validated_data["status"]
        )

        if status_value == "paid":
            order = (
                OrderStatusService.mark_as_paid(
                    order=order
                )
            )

        elif status_value == "shipped":
            order = (
                OrderStatusService.mark_as_shipped(
                    order=order
                )
            )

        elif status_value == "completed":
            order = (
                OrderStatusService
                .mark_as_completed(
                    order=order
                )
            )

        elif status_value == "cancelled":
            order = (
                OrderStatusService.cancel_order(
                    order=order,
                    reason=serializer.validated_data.get(
                        "cancellation_reason",
                        "",
                    ),
                )
            )

        return Response(
            OrderDetailSerializer(order).data
        )