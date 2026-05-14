from django.contrib import admin
from apps.shop_products.models import ShopProduct


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ('shop', 'product', 'price', 'stock', 'is_available')
    list_filter = ('shop', 'product', 'is_available')
    search_fields = ('shop__name', 'product__name')
