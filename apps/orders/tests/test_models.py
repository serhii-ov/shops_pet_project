import pytest
from decimal import Decimal

from apps.orders.models import Order, OrderItem


@pytest.mark.django_db
def test_order_total_price(user, shop):

    order = Order.objects.create(
        user=user,
        shop=shop,
        customer_name="John",
        customer_email="john@example.com",
        customer_phone="123456",
        customer_address="Street 1",
    )

    OrderItem.objects.create(
        order=order,
        product_name="Product 1",
        quantity=2,
        price=Decimal("10.00"),
    )

    OrderItem.objects.create(
        order=order,
        product_name="Product 2",
        quantity=1,
        price=Decimal("5.00"),
    )

    assert order.total_price == Decimal("25.00")


@pytest.mark.django_db
def test_order_total_items(user, shop):

    order = Order.objects.create(
        user=user,
        shop=shop,
        customer_name="John",
        customer_email="john@example.com",
        customer_phone="123456",
        customer_address="Street 1",
    )

    OrderItem.objects.create(
        order=order,
        product_name="Product 1",
        quantity=3,
        price=Decimal("10.00"),
    )

    OrderItem.objects.create(
        order=order,
        product_name="Product 2",
        quantity=2,
        price=Decimal("5.00"),
    )

    assert order.total_items == 5


@pytest.mark.django_db
def test_order_item_total_price(user, shop):

    order = Order.objects.create(
        user=user,
        shop=shop,
        customer_name="John",
        customer_email="john@example.com",
        customer_phone="123456",
        customer_address="Street 1",
    )

    item = OrderItem.objects.create(
        order=order,
        product_name="Product",
        quantity=3,
        price=Decimal("15.00"),
    )

    assert item.total_price == Decimal("45.00")
