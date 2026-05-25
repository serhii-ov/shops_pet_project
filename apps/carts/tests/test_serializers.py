import pytest

from apps.carts.serializers import CartItemSerializer
from apps.carts.tests.factories import (
    ShopProductFactory,
)


@pytest.mark.django_db
def test_cart_item_serializer_valid(shop_product):

    data = {
        "shop_product": shop_product.id,
        "quantity": 2,
    }

    serializer = CartItemSerializer(data=data)

    assert serializer.is_valid()


@pytest.mark.django_db
def test_cart_item_serializer_invalid_stock(shop_product):

    data = {
        "shop_product": shop_product.id,
        "quantity": 999,
    }

    serializer = CartItemSerializer(data=data)

    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
def test_cart_item_serializer_unavailable_product():

    product = ShopProductFactory(
        is_available=False
    )

    data = {
        "shop_product": product.id,
        "quantity": 1,
    }

    serializer = CartItemSerializer(data=data)

    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors
