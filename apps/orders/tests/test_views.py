import pytest
from django.urls import reverse

from apps.orders.models import Order


@pytest.mark.django_db
def test_create_order_view(
    api_client,
    user,
    shop,
    cart,
    cart_item,
):

    api_client.force_authenticate(user=user)

    url = reverse(
        "create-order",
        kwargs={"shop_id": shop.id},
    )

    payload = {
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "customer_phone": "123456789",
        "customer_address": "Some Address",
    }

    response = api_client.post(url, payload)

    assert response.status_code == 200
    assert Order.objects.count() == 1

    data = response.json()

    assert data["customer_name"] == "John Doe"
    assert data["total_items"] == 2


@pytest.mark.django_db
def test_order_detail_view(
    api_client,
    user,
    shop,
):

    order = Order.objects.create(
        user=user,
        shop=shop,
        customer_name="John",
        customer_email="john@example.com",
        customer_phone="123456",
        customer_address="Address",
    )

    api_client.force_authenticate(user=user)

    url = reverse(
        "order-detail",
        kwargs={"id": order.id},
    )

    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == str(order.id)


@pytest.mark.django_db
def test_order_detail_forbidden_for_another_user(
    api_client,
    user,
    another_user,
    shop,
):

    order = Order.objects.create(
        user=user,
        shop=shop,
        customer_name="John",
        customer_email="john@example.com",
        customer_phone="123456",
        customer_address="Address",
    )

    api_client.force_authenticate(
        user=another_user
    )

    url = reverse(
        "order-detail",
        kwargs={"id": order.id},
    )

    response = api_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_orders_list_view(
    api_client,
    user,
    another_user,
    shop,
):

    Order.objects.create(
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

    api_client.force_authenticate(user=user)

    url = reverse("order-history")

    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert len(data['results']) == 1
    assert data['results'][0]["customer_name"] == "John"
