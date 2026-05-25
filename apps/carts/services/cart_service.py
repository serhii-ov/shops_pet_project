"""
What belongs in services?
Business logic:
get/create cart
add item
update quantity
remove item
merge guest cart into user cart
clear cart
deactivate cart
"""
from django.db import transaction

from apps.carts.models import Cart, CartItem


class CartService:

    @staticmethod
    def get_or_create_cart(
        *,
        user=None,
        session_key=None,
        shop,
    ):

        if user and user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(
                user=user,
                shop=shop,
                is_active=True,
            )
        else:
            cart, _ = Cart.objects.get_or_create(
                session_key=session_key,
                shop=shop,
                is_active=True,
            )

        return cart

    @staticmethod
    @transaction.atomic
    def add_item(
        *,
        cart,
        shop_product,
        quantity,
    ):

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            shop_product=shop_product,
            defaults={
                'quantity': quantity,
            }
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.full_clean()
            cart_item.save()

        return cart_item

    @staticmethod
    @transaction.atomic
    def update_item_quantity(
        *,
        cart_item,
        quantity,
    ):

        cart_item.quantity = quantity
        cart_item.full_clean()
        cart_item.save()

        return cart_item

    @staticmethod
    @transaction.atomic
    def remove_item(
        *,
        cart_item,
    ):

        cart_item.delete()
