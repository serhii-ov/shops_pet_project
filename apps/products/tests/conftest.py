import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.users.models.user import User
from apps.categories.models import Category
from apps.products.models import Product


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        email='admin@test.com',
        password='password123',
    )


@pytest.fixture
def regular_user():
    return User.objects.create_user(
        email='user@test.com',
        password='password123',
    )


@pytest.fixture
def category():
    return Category.objects.create(name='Electronics')


@pytest.fixture
def product(category):
    return Product.objects.create(
        name='iPhone',
        description='Smartphone',
        category=category,
    )