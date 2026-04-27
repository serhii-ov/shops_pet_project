import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(
            email=kwargs.get("email", "user@test.com"),
            password=kwargs.get("password", "test12345"),
            first_name="Test",
            last_name="User",
        )
    return make_user


@pytest.fixture
def auth_client(api_client, create_user):
    user = create_user()
    response = api_client.post("/users/auth/login/", {
        "email": user.email,
        "password": "test12345"
    })
    
    token = response.data["access"]

    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client, user
