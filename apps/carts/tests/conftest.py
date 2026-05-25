import pytest
from rest_framework.test import APIClient

from apps.carts.tests.factories import (
    UserFactory,
    ShopFactory,
    ShopProductFactory,
    CartFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def shop():
    return ShopFactory()


@pytest.fixture
def shop_product(shop):
    return ShopProductFactory(shop=shop)


@pytest.fixture
def cart(user, shop):
    return CartFactory(user=user, shop=shop)
