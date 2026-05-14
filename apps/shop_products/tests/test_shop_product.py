from decimal import Decimal
import pytest
from django.urls import reverse
from rest_framework import status

from apps.shop_products.models import ShopProduct


pytestmark = pytest.mark.django_db


def test_list_shop_products(api_client, shop_product):
    url = reverse('shop-product-list')

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


def test_retrieve_shop_product(api_client, shop_product):
    url = reverse(
        'shop-product-detail',
        args=[shop_product.id]
    )

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['product_name'] == 'iPhone 15'


def test_admin_can_create_shop_product(
    api_client,
    admin_user,
    shop,
    second_product
):
    api_client.force_authenticate(admin_user)

    url = reverse('shop-product-list')

    payload = {
        'shop': shop.id,
        'product': second_product.id,
        'price': '899.99',
        'stock': 3,
        'is_available': True
    }

    response = api_client.post(url, payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert ShopProduct.objects.count() == 1


def test_regular_user_cannot_create_shop_product(
    api_client,
    regular_user,
    shop,
    second_product
):
    api_client.force_authenticate(regular_user)

    url = reverse('shop-product-list')

    payload = {
        'shop': shop.id,
        'product': second_product.id,
        'price': '699.99',
        'stock': 10,
        'is_available': True
    }

    response = api_client.post(url, payload)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_can_update_shop_product(
    api_client,
    admin_user,
    shop_product,
    shop,
    product
):
    api_client.force_authenticate(admin_user)

    url = reverse(
        'shop-product-detail',
        args=[shop_product.id]
    )

    payload = {
        'shop': shop.id,
        'product': product.id,
        'price': '899.99',
        'stock': 2,
        'is_available': False
    }

    response = api_client.put(url, payload)

    shop_product.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert shop_product.price == Decimal('899.99')
    assert shop_product.stock == 2
    assert shop_product.is_available is False


def test_admin_can_delete_shop_product(
    api_client,
    admin_user,
    shop_product
):
    api_client.force_authenticate(admin_user)

    url = reverse(
        'shop-product-detail',
        args=[shop_product.id]
    )

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ShopProduct.objects.count() == 0


def test_filter_by_shop(
    api_client,
    shop,
    shop_product
):
    url = reverse('shop-product-list')

    response = api_client.get(
        f'{url}?shop={shop.id}'
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


def test_duplicate_shop_product_not_allowed(
    api_client,
    admin_user,
    shop,
    product,
    shop_product
):
    api_client.force_authenticate(admin_user)

    url = reverse('shop-product-list')

    payload = {
        'shop': shop.id,
        'product': product.id,
        'price': '1000.00',
        'stock': 1,
        'is_available': True
    }

    response = api_client.post(url, payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
