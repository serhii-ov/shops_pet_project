import pytest

from apps.products.models import Product
from apps.categories.models import Category


@pytest.mark.django_db
def test_product_slug_is_created_automatically():
    category = Category.objects.create(name='Electronics')

    product = Product.objects.create(
        name='iPhone 15 Pro',
        category=category,
    )

    assert product.slug == 'iphone-15-pro'


@pytest.mark.django_db
def test_product_str_returns_name():
    category = Category.objects.create(name='Electronics')

    product = Product.objects.create(
        name='MacBook',
        category=category,
    )

    assert str(product) == 'MacBook'
