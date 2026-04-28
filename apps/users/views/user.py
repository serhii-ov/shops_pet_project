from rest_framework import viewsets, views
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from apps.users.serializers import (
    UserSerializer, 
    AdminUserSerializer,
    )
from apps.users.permissions import UserPermission


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("profile")
    permission_classes = [UserPermission]

    def get_serializer_class(self):
        user = self.request.user

        if user.is_superuser or \
            user.groups.filter(name__in=["Admin"]).exists():
            
            return AdminUserSerializer
        return UserSerializer
    

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.queryset
        return self.queryset.filter(id=user.id)


class MeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
