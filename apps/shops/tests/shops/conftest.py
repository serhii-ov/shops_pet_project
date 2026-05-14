import pytest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

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
def customer_group():
    group, _ = Group.objects.get_or_create(name="Customer")
    return group


@pytest.fixture
def customer_user(django_user_model, customer_group):
    user = django_user_model.objects.create_user(
        email="customer@example.com",
        password="pass123"
    )
    user.groups.add(customer_group)
    return user


@pytest.fixture
def shop(db):
    return Shop.objects.create(
        name='Tech Store'
    )


@pytest.fixture
def shops():
    shop1 = Shop.objects.create(
        name='Shop 1',
        average_rating=2.5
    )
    shop2 = Shop.objects.create(
        name='Shop 2',
        average_rating=4.0
    )
    shop3 = Shop.objects.create(
        name='Shop 3',
        average_rating=5.0
    )

    return [shop1, shop2, shop3]
