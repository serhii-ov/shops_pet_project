from django.urls import path

from apps.carts.views import (
    CartDetailView,
    AddCartItemView,
    CartItemUpdateView,
    CartItemDeleteView,
)

urlpatterns = [

    path(
        '<int:shop_id>/',
        CartDetailView.as_view(),
        name='cart-detail',
    ),

    path(
        '<int:shop_id>/items/',
        AddCartItemView.as_view(),
        name='cart-add-item',
    ),

    path(
        'cart-items/<int:pk>/',
        CartItemUpdateView.as_view(),
        name='cart-item-update',
    ),

    path(
        'cart-items/<int:pk>/delete/',
        CartItemDeleteView.as_view(),
        name='cart-item-delete',
    ),
]
