from django.urls import path

from apps.orders.views import (
    CreateOrderView,
    OrderDetailView,
    UserOrdersListView,
)

urlpatterns = [

    path(
        "shops/<int:shop_id>/create-order/",
        CreateOrderView.as_view(),
        name="create-order",
    ),

    path(
        "order-history/",
        UserOrdersListView.as_view(),
        name="order-history",
    ),

    path(
        "orders/<uuid:id>/",
        OrderDetailView.as_view(),
        name="order-detail",
    ),
]
