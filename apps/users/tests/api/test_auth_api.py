import pytest
from apps.users.models import UserSession
 

@pytest.mark.django_db
def test_login(api_client, create_user):
    user = create_user()

    response = api_client.post("/users/auth/login/", {
        "email": user.email,
        "password": "test12345"
    })

    assert response.status_code == 200
    assert "access" in response.json()
    assert "refresh" in response.json()

    assert UserSession.objects.filter(user=user).exists()
    

@pytest.mark.django_db
def test_refresh_token(api_client, create_user):
    user = create_user()

    login = api_client.post("/users/auth/login/", {
        "email": user.email,
        "password": "test12345"
    })

    refresh = login.data["refresh"]

    response = api_client.post("/users/auth/refresh/", {
        "refresh": refresh
    })

    assert response.status_code == 200
    assert "access" in response.json()


@pytest.mark.django_db
def test_logout(api_client, create_user):
    user = create_user()

    login = api_client.post("/users/auth/login/", {
        "email": user.email,
        "password": "test12345"
    })

    refresh = login.data["refresh"]

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {login.data['access']}"
    )

    response = api_client.post("/users/auth/logout/", {
        "refresh": refresh
    })

    assert response.status_code == 200

    from apps.users.models import UserSession
    assert UserSession.objects.filter(
        user=user,
        is_active=False
    ).exists()


@pytest.mark.django_db
def test_logout_all(auth_client):
    client, user = auth_client

    # create multiple sessions
    client.post("/users/auth/login/", {
        "email": user.email,
        "password": "test12345"
    })

    response = client.post("/users/auth/logout_all/")

    assert response.status_code == 200
    assert not user.sessions.filter(is_active=True).exists()


@pytest.mark.django_db
def test_invalid_login(api_client):
    response = api_client.post("/users/auth/login/", {
        "email": "wrong@test.com",
        "password": "wrong"
    })

    assert response.status_code == 401


@pytest.mark.django_db
def test_invalid_refresh(api_client):
    response = api_client.post("/users/auth/refresh/", {
        "refresh": "invalid"
    })

    assert response.status_code == 401
