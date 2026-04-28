from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.models import UserSession


class AuthService:

    @staticmethod
    def login(*, user, request):
        refresh = RefreshToken.for_user(user)

        UserSession.objects.create(
            user=user,
            refresh_token_jti=refresh["jti"],
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            ip_address=AuthService.get_client_ip(request),
        )

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    def logout(*, refresh_token):
        token = RefreshToken(refresh_token)
        jti = token["jti"]

        UserSession.objects.filter(
            refresh_token_jti=jti
        ).update(is_active=False)

        token.blacklist()

    @staticmethod
    def validate_session(refresh_token: str):
        try:
            token = RefreshToken(refresh_token)
            jti = token["jti"]

            session = UserSession.objects.filter(
                refresh_token_jti=jti,
                is_active=True
            ).first()

            if not session:
                raise ValueError("Session expired or revoked")

            session.save(update_fields=["last_used_at"])
            return token
        except TokenError as e:
            raise ValueError("Invalid session token") from e

    @staticmethod
    def get_client_ip(request):
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded:
            return x_forwarded.split(",")[0]
        return request.META.get("REMOTE_ADDR")
    
    @staticmethod
    def logout_all(*, user):
        user.sessions.filter(is_active=True).update(is_active=False)
