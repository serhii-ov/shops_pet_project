from rest_framework import serializers

from apps.orders.models import Order
from apps.orders.serializers.order_item_serializer import (
    OrderItemSerializer,
)
from apps.orders.services.order_service import (
    OrderService,
)


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'total_price',
            'items',
            'created_at',
        ]

        read_only_fields = [
            'user',
            'total_price',
            'created_at',
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        
        return OrderService.create_order(user)
# from decimal import Decimal

# from django.db import transaction
# from rest_framework import serializers

# from apps.orders.serializers.order_item_serializer import (
#     OrderItemSerializer,
#     )
# from apps.orders.models import Order, OrderItem
# from apps.carts.models import CartItem


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Order
#         fields = [
#             'id',
#             'user',
#             'status',
#             'total_price',
#             'items',
#             'created_at',
#         ]

#         read_only_fields = [
#             'user',
#             'total_price',
#             'created_at',
#         ]

#     @transaction.atomic
#     def create(self, validated_data):

#         user = self.context['request'].user

#         cart_items = CartItem.objects.select_related(
#             'shop_product'
#         ).filter(
#             cart__user=user
#         )

#         if not cart_items.exists():
#             raise serializers.ValidationError(
#                 'Cart is empty.'
#             )

#         order = Order.objects.create(
#             user=user
#         )

#         total_price = Decimal('0.00')

#         for cart_item in cart_items:

#             shop_product = cart_item.shop_product

#             if not shop_product.is_available:
#                 raise serializers.ValidationError(
#                     f'{shop_product.product.name} is unavailable.'
#                 )

#             if cart_item.quantity > shop_product.stock:
#                 raise serializers.ValidationError(
#                     f'Not enough stock for {shop_product.product.name}.'
#                 )

#             OrderItem.objects.create(
#                 order=order,
#                 shop_product=shop_product,
#                 quantity=cart_item.quantity,
#                 price=shop_product.price,
#             )

#             shop_product.stock -= cart_item.quantity

#             if shop_product.stock <= 0:
#                 shop_product.stock = 0
#                 shop_product.is_available = False

#             shop_product.save()

#             total_price += (
#                 shop_product.price * cart_item.quantity
#             )

#         order.total_price = total_price
#         order.status = Order.COMPLETED
#         order.save()

#         cart_items.delete()

#         return order
