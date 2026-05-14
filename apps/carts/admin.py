from django.contrib import admin

from .models.cart_model import Cart
from .models.cart_item_model import CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('created_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'shop_product', 'quantity')
    search_fields = ('cart__user__username', 'shop_product__product__name')
    list_filter = ('quantity',)
