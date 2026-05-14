from django.urls import path

from .views import (
    ShopListCreateView,
    ShopRetrieveUpdateDestroyView,
    ShopRatingCreateView,
    CustomerRatingHistoryView,
)


urlpatterns = [
    path('', ShopListCreateView.as_view(), name='shop-list-create'),

    path(
        '<int:pk>/',
        ShopRetrieveUpdateDestroyView.as_view(),
        name='shop-detail'
    ),

    path(
        'rate/',
        ShopRatingCreateView.as_view(),
        name='shop-rate'
    ),

    path(
        'my-ratings/',
        CustomerRatingHistoryView.as_view(),
        name='customer-rating-history'
    ),
    path(
        'customer-ratings/<int:customer_id>/',
        CustomerRatingHistoryView.as_view(),
        name='customer-rating-history'
    ),
]
