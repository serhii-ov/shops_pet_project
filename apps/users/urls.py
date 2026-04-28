from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, 
    LoginView, 
    LogoutView,
    LogoutAllView,
    RefreshView,
    MeView,
    SessionListView,
    RevokeSessionView,
    )

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", RefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/logout_all/", LogoutAllView.as_view(), name="logout_all"),
    path("me/", MeView.as_view(), name="me"),

    path("sessions/", SessionListView.as_view(), name="session-list"),
    path("sessions/<uuid:id>/", RevokeSessionView.as_view(), name="session-revoke"),
]

urlpatterns += router.urls
