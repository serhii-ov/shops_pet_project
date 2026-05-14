import pytest

from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.categories.models import Category


@pytest.mark.django_db
def test_product_serializer_contains_expected_fields():
    category = Category.objects.create(name='Electronics')

    product = Product.objects.create(
        name='Laptop',
        description='Gaming laptop',
        category=category,
    )

    serializer = ProductSerializer(product)

    data = serializer.data

    assert set(data.keys()) == {
        'id',
        'name',
        'slug',
        'description',
        'image',
        'category',
        'category_name',
        'created_at',
        'updated_at',
    }

    assert data['category_name'] == 'Electronics'
