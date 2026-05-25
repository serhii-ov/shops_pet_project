import pytest
from rest_framework import status

from apps.carts.models.cart_item_model import CartItem
from apps.carts.tests.factories import (
    CartItemFactory,
)


@pytest.mark.django_db
def test_get_cart(
    api_client,
    cart,
):

    response = api_client.get(
        f"/carts/{cart.shop.id}/"
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_add_cart_item(
    api_client,
    cart,
    shop_product,
):

    session = api_client.session
    session.save()

    response = api_client.post(
        f"/carts/{cart.shop.id}/items/",
        {
            "shop_product": shop_product.id,
            "quantity": 2,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.data["items"]) == 1


@pytest.mark.django_db
def test_update_cart_item(
    api_client,
    cart,
):

    item = CartItemFactory(cart=cart)

    response = api_client.patch(
        f"/carts/cart-items/{item.id}/",
        {
            "quantity": 5,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    item.refresh_from_db()

    assert item.quantity == 5


@pytest.mark.django_db
def test_delete_cart_item(
    api_client,
    cart,
):

    item = CartItemFactory(cart=cart)

    response = api_client.delete(
        f"/carts/cart-items/{item.id}/delete/"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(CartItem.DoesNotExist):
        item.refresh_from_db()
