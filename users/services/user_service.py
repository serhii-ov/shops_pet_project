from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from users.models import Profile

User = get_user_model()


class UserService:

    @staticmethod
    @transaction.atomic
    def create_user(*, email, password, first_name="", last_name="", profile_data=None):
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        Profile.objects.update_or_create(
            user=user,
            defaults=profile_data or {}
        )
        return user

    # @staticmethod
    # @transaction.atomic
    # def create_user(
    #     *, email, 
    #     password, 
    #     first_name="", 
    #     last_name="", 
    #     profile_data=None
    #     ):
    #     user = User.objects.create_user(
    #         email=email,
    #         password=password,
    #         first_name=first_name,
    #         last_name=last_name,
    #     )

    #     if profile_data:
    #         Profile.objects.update_or_create(
    #             user=user,
    #             defaults=profile_data
    #         )

    #     return user

    @staticmethod
    @transaction.atomic
    def update_user(*, user, data, profile_data=None):
        password = data.pop("password", None)

        for attr, value in data.items():
            setattr(user, attr, value)

        if password:
            user.set_password(password)

        user.save()

        if profile_data is not None:
            profile, _ = Profile.objects.get_or_create(user=user)

            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return user

    @staticmethod
    def assign_groups(*, user, groups):
        user.groups.set(groups)
        return user
