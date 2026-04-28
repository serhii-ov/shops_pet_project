import pytest
from apps.users.services.auth_service import AuthService
from apps.users.models import UserSession


@pytest.mark.django_db
def test_login_creates_session(user, rf):
    request = rf.post("/")
    request.META["REMOTE_ADDR"] = "127.0.0.1"

    tokens = AuthService.login(user=user, request=request)

    assert "access" in tokens
    assert "refresh" in tokens
    assert UserSession.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_logout_deactivates_session(user, rf):
    request = rf.post("/")
    tokens = AuthService.login(user=user, request=request)

    refresh = tokens["refresh"]

    AuthService.logout(refresh_token=refresh)

    assert UserSession.objects.filter(
        user=user,
        is_active=False
    ).exists()


@pytest.mark.django_db
def test_logout_all(user, rf):
    request = rf.post("/")
    AuthService.login(user=user, request=request)
    AuthService.login(user=user, request=request)

    AuthService.logout_all(user=user)

    assert not user.sessions.filter(is_active=True).exists()


@pytest.mark.django_db
def test_validate_session_valid(user, rf):
    request = rf.post("/")
    tokens = AuthService.login(user=user, request=request)

    token = AuthService.validate_session(
        refresh_token=tokens["refresh"]
    )

    assert token is not None


@pytest.mark.django_db
def test_validate_session_invalid():
    with pytest.raises(ValueError):
        AuthService.validate_session(refresh_token="invalid_token")
