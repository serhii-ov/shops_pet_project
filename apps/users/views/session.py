from rest_framework import generics, permissions

from apps.users.models import UserSession
from apps.users.serializers import SessionSerializer


class SessionListView(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user,
            is_active=True
        )


class RevokeSessionView(generics.DestroyAPIView):
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user,
            is_active=True
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
