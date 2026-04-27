from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, 
    TokenRefreshSerializer,
    )
from rest_framework import serializers

from users.services.auth_service import AuthService


class CustomTokenObtainPairSerializer(
    TokenObtainPairSerializer
    ):
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["is_staff"] = user.is_staff

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        tokens = AuthService.login(
            user=self.user,
            request=self.context["request"]
        )

        return tokens

    def get_client_ip(self, request):
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded:
            return x_forwarded.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        try:
            AuthService.validate_session(
                refresh_token=attrs["refresh"]
            )
        except ValueError:
            raise serializers.ValidationError("Session expired or revoked")

        return super().validate(attrs)
