import pytest

from apps.carts.selectors.cart_selectors import (
    get_cart_with_items,
)
from apps.carts.tests.factories import (
    CartFactory,
    CartItemFactory,
)


@pytest.mark.django_db
def test_get_cart_with_items():

    cart = CartFactory()

    CartItemFactory.create_batch(
        3,
        cart=cart,
    )

    result = get_cart_with_items(cart.id)

    assert result.id == cart.id
    assert result.items.count() == 3