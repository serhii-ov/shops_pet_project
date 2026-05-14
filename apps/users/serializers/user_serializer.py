from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.users.services.user_service import UserService
from apps.users.models import Profile


User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["phone", "address", "avatar"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id", 
            "email", 
            "password", 
            "first_name", 
            "last_name", 
            "profile",
            ]

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)

        return UserService.create_user(
            profile_data=profile_data,
            **validated_data
        )

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)

        return UserService.update_user(
            user=instance,
            data=validated_data,
            profile_data=profile_data
        )


class AdminUserSerializer(UserSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        many=True,
        required=False
    )

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ["groups"]

    def update(self, instance, validated_data):
        groups = validated_data.pop("groups", None)

        user = super().update(instance, validated_data)

        if groups is not None:
            UserService.assign_groups(user=user, groups=groups)

        return user

    def validate_groups(self, value):
        request = self.context.get("request")

        if not request or not request.user.is_superuser:
            raise serializers.ValidationError(
                "Only superusers can assign groups"
            )
        return value
