from rest_framework import views, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from users.serializers import (
    CustomTokenObtainPairSerializer,
    )
from users.models import UserSession


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RefreshView(TokenRefreshView):
    pass


class LogoutView(views.APIView):
    """Class implements logout from a single device."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token required"}, 
                status=400,
                )

        token = RefreshToken(refresh_token)
        jti = token["jti"]

        # deactivate session
        UserSession.objects.filter(
            refresh_token_jti=jti
        ).update(is_active=False)

        token.blacklist()

        return Response({"detail": "Logged out"})


class LogoutAllView(views.APIView):
    """Class implements logout from all devices."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sessions = request.user.sessions.filter(is_active=True)

        for session in sessions:
            session.is_active = False
            session.save()

        return Response({"detail": "Logged out from all devices"})
