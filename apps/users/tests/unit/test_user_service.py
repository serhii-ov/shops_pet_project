import pytest
from apps.users.services.user_service import UserService


@pytest.mark.django_db
def test_create_user(user_data):
    user = UserService.create_user(**user_data)

    assert user.email == user_data["email"]
    assert user.check_password(user_data["password"])
    assert user.first_name == user_data["first_name"]


@pytest.mark.django_db
def test_create_user_with_profile(user_data):
    profile_data = {
        "phone": "123456789",
        "address": "Test street",
    }

    user = UserService.create_user(
        **user_data,
        profile_data=profile_data
    )

    assert user.profile.phone == "123456789"
    assert user.profile.address == "Test street"


@pytest.mark.django_db
def test_update_user(user):
    updated = UserService.update_user(
        user=user,
        data={"first_name": "Updated"}
    )

    assert updated.first_name == "Updated"


@pytest.mark.django_db
def test_update_user_password(user):
    UserService.update_user(
        user=user,
        data={"password": "newpass123"}
    )

    assert user.check_password("newpass123")


@pytest.mark.django_db
def test_update_user_profile(user):
    profile_data = {
        "phone": "999999",
    }

    UserService.update_user(
        user=user,
        data={},
        profile_data=profile_data
    )

    assert user.profile.phone == "999999"


@pytest.mark.django_db
def test_assign_groups(user):
    from django.contrib.auth.models import Group

    group = Group.objects.create(name="TestGroup")

    UserService.assign_groups(user=user, groups=[group])

    assert user.groups.filter(name="TestGroup").exists()


@pytest.mark.django_db
def test_update_user_without_profile_does_not_crash(user):
    UserService.update_user(user=user, data={})
    assert user is not None


@pytest.mark.django_db
def test_create_user_without_profile(user_data):
    user = UserService.create_user(**user_data)
    assert user.profile  # if auto-created elsewhere OR handle accordingly
