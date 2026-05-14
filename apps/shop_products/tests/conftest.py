import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.products.models import Product
from apps.shop_products.models import ShopProduct
from apps.shops.models import Shop


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_group():
    group, _ = Group.objects.get_or_create(name="Admin")
    return group


@pytest.fixture
def admin_user(django_user_model, admin_group):
    user = django_user_model.objects.create_user(
        email="admin@example.com",
        password="pass123"
    )
    user.groups.add(admin_group)
    return user


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        email='user@test.com',
        password='user123'
    )


@pytest.fixture
def shop(db):
    return Shop.objects.create(
        name='Tech Store'
    )


@pytest.fixture
def category(db):
    return Category.objects.create(
        name='Phones'
    )


@pytest.fixture
def product(category):
    return Product.objects.create(
        name='iPhone 15',
        slug='iphone-15',
        category=category,
    )


@pytest.fixture
def second_product(category):
    return Product.objects.create(
        name='Samsung S24',
        slug='samsung-s24',
        category=category,
    )


@pytest.fixture
def shop_product(shop, product):
    return ShopProduct.objects.create(
        shop=shop,
        product=product,
        price=999.99,
        stock=5,
        is_available=True
    )
