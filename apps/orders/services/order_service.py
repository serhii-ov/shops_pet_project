from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.core.exceptions import ValidationError

from apps.orders.models import (
    Order,
    OrderItem,
)
from apps.shop_products.models import ShopProduct


def recalculate_order_totals(order):
    items = order.items.all()

    order.total_price = sum(
        (item.total_price for item in items),
        Decimal("0.00"),
    )

    order.total_items = sum(
        item.quantity for item in items
    )

    order.save(
        update_fields=[
            "total_price",
            "total_items",
            "total",
        ]
    )

class OrderService:

    @staticmethod
    @transaction.atomic
    def create_order_from_cart(
        *,
        cart,
        customer_name,
        customer_email,
        customer_phone,
        customer_address,
    ):
        cart_items = list(
            cart.items.select_related("shop_product")
        )
        if not cart_items:
            raise ValidationError("Cannot create order from empty cart.")
        
        order = Order.objects.create(
            user=cart.user,
            shop=cart.shop,

            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_address=customer_address,
        )

        order_items = []

        for cart_item in cart.items.select_related(
            "shop_product"
        ):
            order_items.append(
                OrderItem(
                    order=order,
                    shop_product=cart_item.shop_product,
                    quantity=cart_item.quantity,
                    product_name=cart_item.product_name,
                    price=cart_item.price,
                )
            )

            # reduce stock
            shop_product = cart_item.shop_product
       
            updated = ShopProduct.objects.filter(
                pk=shop_product.pk,
                stock__gte=cart_item.quantity,
            ).update(
                stock=F("stock") - cart_item.quantity
            )

            if not updated:
                raise ValidationError("Insufficient stock")
            
        OrderItem.objects.bulk_create(order_items)
        recalculate_order_totals(order)

        # deactivate cart
        cart.is_active = False
        cart.save(update_fields=["is_active"])

        return order
