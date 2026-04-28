import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "strongpass123",
        "first_name": "John",
        "last_name": "Doe",
    }


@pytest.fixture
def user(db, user_data):
    return User.objects.create_user(**user_data)
