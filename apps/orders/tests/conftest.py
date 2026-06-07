import pytest
from decimal import Decimal

from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from apps.products.models import Product
from apps.categories.models import Category
from apps.shops.models import Shop
from apps.shop_products.models import ShopProduct
from apps.carts.models import Cart, CartItem

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="test@example.com",
        password="password123",
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        email="another@example.com",
        password="password123",
    )


@pytest.fixture
def shop(db):
    return Shop.objects.create(
        name="Test Shop",
    )


@pytest.fixture
def shop_product(db, shop):
    category = Category.objects.create(
        name="Electronics",
    )
    product=Product.objects.create(
            name="iPhone",
            category=category,
        )
    return ShopProduct.objects.create(
        shop=shop,
        product=product,
        price=Decimal("1000.00"),
        stock=10,
    )


@pytest.fixture
def cart(db, user, shop):
    return Cart.objects.create(
        user=user,
        shop=shop,
        is_active=True,
    )


@pytest.fixture
def cart_item(db, cart, shop_product):
    return CartItem.objects.create(
        cart=cart,
        shop_product=shop_product,
        quantity=2,
        product_name=shop_product.product.name,
        price=shop_product.price,
    )
