import pytest

from apps.products.models import Product
from apps.categories.models import Category


@pytest.mark.django_db
def test_list_products(api_client, product):
    response = api_client.get('/products/')

    assert response.status_code == 200
    assert len(response.data['results']) == 1


@pytest.mark.django_db
def test_retrieve_product(api_client, product):
    response = api_client.get(f'/products/{product.id}/')

    assert response.status_code == 200
    assert response.data['name'] == 'iPhone'


@pytest.mark.django_db
def test_admin_can_create_product(api_client, admin_user, category):
    api_client.force_authenticate(user=admin_user)

    payload = {
        'name': 'Samsung Galaxy',
        'description': 'Android phone',
        'category': category.id,
    }

    response = api_client.post('/products/', payload)

    assert response.status_code == 201
    assert Product.objects.count() == 1
    assert Product.objects.first().slug == 'samsung-galaxy'


@pytest.mark.django_db
def test_regular_user_cannot_create_product(
    api_client,
    regular_user,
    category,
):
    api_client.force_authenticate(user=regular_user)

    payload = {
        'name': 'Samsung Galaxy',
        'description': 'Android phone',
        'category': category.id,
    }

    response = api_client.post('/products/', payload)

    assert response.status_code == 403


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_product(
    api_client,
    category,
):
    payload = {
        'name': 'Samsung Galaxy',
        'description': 'Android phone',
        'category': category.id,
    }

    response = api_client.post('/products/', payload)

    assert response.status_code == 401


@pytest.mark.django_db
def test_admin_can_update_product(
    api_client,
    admin_user,
    product,
):
    api_client.force_authenticate(user=admin_user)

    payload = {
        'name': 'Updated iPhone',
        'description': 'Updated description',
        'category': product.category.id,
    }

    response = api_client.put(
        f'/products/{product.id}/',
        payload,
    )

    assert response.status_code == 200

    product.refresh_from_db()

    assert product.name == 'Updated iPhone'


@pytest.mark.django_db
def test_admin_can_delete_product(
    api_client,
    admin_user,
    product,
):
    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(f'/products/{product.id}/')

    assert response.status_code == 204
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_filter_products_by_category(
    api_client,
    category,
):
    another_category = Category.objects.create(name='Books')

    Product.objects.create(
        name='Laptop',
        category=category,
    )

    Product.objects.create(
        name='Python Book',
        category=another_category,
    )

    response = api_client.get(
        f'/products/?category={category.id}'
    )

    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == 'Laptop'
