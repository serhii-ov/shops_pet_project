from django.contrib import admin

from apps.orders.models.order_model import Order
from apps.orders.models.order_item_model import OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin): 
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'shop_product', 'quantity', 'price')
    list_filter = ('order', 'shop_product')
    search_fields = ('order__id', 'shop_product__name')
