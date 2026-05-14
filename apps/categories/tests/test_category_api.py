import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.categories.models import Category
from apps.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        email='admin@example.com',
        password='testpass123',
    )


@pytest.fixture
def regular_user():
    return User.objects.create_user(
        email='user@example.com',
        password='testpass123',
    )


@pytest.mark.django_db
class TestCategoryAPI:

    def test_get_categories_allow_any(self, api_client):
        Category.objects.create(name='Books')
        Category.objects.create(name='Electronics')

        response = api_client.get('/categories/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_create_category_admin_only(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)

        payload = {
            'name': 'Sports'
        }

        response = api_client.post('/categories/', payload)

        assert response.status_code == status.HTTP_201_CREATED
        assert Category.objects.filter(name='Sports').exists()

    def test_create_category_denied_for_anonymous(self, api_client):
        payload = {
            'name': 'Gaming'
        }

        response = api_client.post('/categories/', payload)

        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ]

    def test_create_category_denied_for_regular_user(
        self,
        api_client,
        regular_user,
    ):
        api_client.force_authenticate(user=regular_user)

        payload = {
            'name': 'Movies'
        }

        response = api_client.post('/categories/', payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN
