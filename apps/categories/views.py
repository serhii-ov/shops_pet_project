from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.users.permissions import IsAdmin
from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
 