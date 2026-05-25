import pytest

from apps.carts.models import CartItem
from apps.carts.services.cart_service import CartService


@pytest.mark.django_db
def test_get_or_create_cart(user, shop):

    cart = CartService.get_or_create_cart(
        user=user,
        shop=shop,
    )

    assert cart.user == user
    assert cart.shop == shop


@pytest.mark.django_db
def test_add_item(cart, shop_product):

    CartService.add_item(
        cart=cart,
        shop_product=shop_product,
        quantity=2,
    )

    item = CartItem.objects.get(cart=cart)

    assert item.quantity == 2


@pytest.mark.django_db
def test_add_existing_item_increments_quantity(
    cart,
    shop_product,
):

    CartService.add_item(
        cart=cart,
        shop_product=shop_product,
        quantity=2,
    )

    CartService.add_item(
        cart=cart,
        shop_product=shop_product,
        quantity=3,
    )

    item = CartItem.objects.get(cart=cart)

    assert item.quantity == 5


@pytest.mark.django_db
def test_update_item_quantity(cart, shop_product):

    item = CartService.add_item(
        cart=cart,
        shop_product=shop_product,
        quantity=2,
    )

    CartService.update_item_quantity(
        cart_item=item,
        quantity=10,
    )

    item.refresh_from_db()

    assert item.quantity == 10


@pytest.mark.django_db
def test_remove_item(cart, shop_product):

    item = CartService.add_item(
        cart=cart,
        shop_product=shop_product,
        quantity=2,
    )

    CartService.remove_item(
        cart_item=item
    )

    assert not CartItem.objects.exists()
