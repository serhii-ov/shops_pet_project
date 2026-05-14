from decimal import Decimal

from django.db import transaction

from rest_framework.exceptions import ValidationError

from apps.orders.models import Order, OrderItem
from apps.carts.models import CartItem


class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order(user):

        cart_items = CartItem.objects.select_related(
            'shop_product',
            'shop_product__product',
        ).filter(
            cart__user=user
        )

        if not cart_items.exists():
            raise ValidationError('Cart is empty.')

        order = Order.objects.create(
            user=user
        )

        total_price = Decimal('0.00')

        for cart_item in cart_items:

            shop_product = cart_item.shop_product

            if not shop_product.is_available:
                raise ValidationError(
                    f'{shop_product.product.name} is unavailable.'
                )

            if cart_item.quantity > shop_product.stock:
                raise ValidationError(
                    f'Not enough stock for '
                    f'{shop_product.product.name}.'
                )

            OrderItem.objects.create(
                order=order,
                shop_product=shop_product,
                quantity=cart_item.quantity,
                price=shop_product.price,
            )

            shop_product.stock -= cart_item.quantity

            if shop_product.stock <= 0:
                shop_product.stock = 0
                shop_product.is_available = False

            shop_product.save()

            total_price += (
                shop_product.price * cart_item.quantity
            )

        order.total_price = total_price
        order.status = Order.COMPLETED
        order.save()

        cart_items.delete()

        return order
    