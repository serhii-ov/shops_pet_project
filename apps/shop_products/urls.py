from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    ShopProductViewSet,
)


router = DefaultRouter()

router.register(
    r'',
    ShopProductViewSet,
    basename='shop-product'
)

urlpatterns = [
    path('', include(router.urls)),
]
