import pytest


@pytest.mark.django_db
def test_create_user(api_client):
    response = api_client.post("/users/users/", {
        "email": "new@test.com",
        "password": "strongpass123",
        "first_name": "New",
        "last_name": "User"
    })

    assert response.status_code == 201


@pytest.mark.django_db
def test_me_endpoint(auth_client):
    client, user = auth_client

    response = client.get("/users/me/")

    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_update_user(auth_client):
    client, user = auth_client

    response = client.patch(f"/users/users/{user.id}/", {
        "first_name": "Updated"
    })

    assert response.status_code == 200
    assert response.data["first_name"] == "Updated"


@pytest.mark.django_db
def test_update_profile(auth_client):
    client, user = auth_client

    response = client.patch(f"/users/users/{user.id}/", {
        "profile": {
            "phone": "123456"
        }
    }, format="json")

    assert response.status_code == 200
    assert response.data["profile"]["phone"] == "123456"


@pytest.mark.django_db
def test_user_cannot_access_others(api_client, create_user):
    user1 = create_user(email="u1@test.com")
    user2 = create_user(email="u2@test.com")

    login = api_client.post("/users/auth/login/", {
        "email": user1.email,
        "password": "test12345"
    })

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {login.data['access']}"
    )

    response = api_client.get(f"/users/{user2.id}/")

    assert response.status_code in [403, 404]


@pytest.mark.django_db
def test_admin_can_access_all(api_client, create_user):
    admin = create_user(email="admin@test.com")
    admin.is_superuser = True
    admin.is_staff = True
    admin.save()

    user = create_user(email="user@test.com")

    login = api_client.post("/users/auth/login/", {
        "email": admin.email,
        "password": "test12345"
    })

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {login.data['access']}"
    )

    response = api_client.get(f"/users/users/{user.id}/")

    assert response.status_code == 200
