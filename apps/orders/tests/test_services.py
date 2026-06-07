import pytest

from apps.orders.models import Order, OrderItem
from apps.orders.services import OrderService


@pytest.mark.django_db
def test_create_order_from_cart(
    cart,
    cart_item,
    shop_product,
):

    order = OrderService.create_order_from_cart(
        cart=cart,
        customer_name="John Doe",
        customer_email="john@example.com",
        customer_phone="123456789",
        customer_address="Some Address",
    )

    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 1

    assert order.customer_name == "John Doe"

    item = order.items.first()

    assert item.product_name == "iPhone"
    assert item.quantity == 2

    shop_product.refresh_from_db()

    assert shop_product.stock == 8

    cart.refresh_from_db()

    assert cart.is_active is False
