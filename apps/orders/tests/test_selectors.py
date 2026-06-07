import pytest

from apps.orders.models import Order
from apps.orders.selectors.order_selectors import (
    get_order_with_items,
    get_user_orders,
)


@pytest.mark.django_db
def test_get_order_with_items(user, shop):

    order = Order.objects.create(
        user=user,
        shop=shop,
        customer_name="John",
        customer_email="john@example.com",
        customer_phone="123",
        customer_address="Address",
    )

    result = get_order_with_items(order.id)

    assert result == order


@pytest.mark.django_db
def test_get_user_orders(user, another_user, shop):

    user_order = Order.objects.create(
        user=user,
        shop=shop,
        customer_name="John",
        customer_email="john@example.com",
        customer_phone="123",
        customer_address="Address",
    )

    Order.objects.create(
        user=another_user,
        shop=shop,
        customer_name="Another",
        customer_email="another@example.com",
        customer_phone="456",
        customer_address="Address",
    )

    qs = get_user_orders(user)

    assert qs.count() == 1
    assert qs.first() == user_order
