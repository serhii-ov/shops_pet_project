import pytest
from decimal import Decimal
from django.core.exceptions import ValidationError

from apps.carts.tests.factories import (
    CartFactory,
    CartItemFactory,
    ShopFactory,
    ShopProductFactory,
)


@pytest.mark.django_db
def test_cart_total_price():

    cart = CartFactory()

    CartItemFactory(
        cart=cart,
        quantity=2,
        price=Decimal("10.00"),
    )

    CartItemFactory(
        cart=cart,
        quantity=1,
        price=Decimal("5.00"),
    )

    assert cart.total_price == Decimal("25.00")


@pytest.mark.django_db
def test_cart_total_items():

    cart = CartFactory()

    CartItemFactory(cart=cart, quantity=2)
    CartItemFactory(cart=cart, quantity=3)

    assert cart.total_items == 5


@pytest.mark.django_db
def test_cart_requires_user_or_session():

    cart = CartFactory.build(
        user=None,
        session_key=None,
    )

    with pytest.raises(ValidationError):
        cart.full_clean()


@pytest.mark.django_db
def test_cart_cannot_have_user_and_session():

    cart = CartFactory.build(
        session_key="abc123"
    )

    with pytest.raises(ValidationError):
        cart.full_clean()


@pytest.mark.django_db
def test_cart_item_shop_validation():

    cart = CartFactory()

    another_shop = ShopFactory()

    shop_product = ShopProductFactory(
        shop=another_shop
    )

    item = CartItemFactory.build(
        cart=cart,
        shop_product=shop_product,
    )

    with pytest.raises(ValidationError):
        item.full_clean()
