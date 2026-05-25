from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
   
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    path('users/', include('apps.users.urls')),
    path('shops/', include('apps.shops.urls')),
    path('shop_products/', include('apps.shop_products.urls')),
    path('categories/', include('apps.categories.urls')),
    path('products/', include('apps.products.urls')),
    path('carts/', include('apps.carts.urls')),
    # path('orders/', include('apps.orders.urls')),
]
