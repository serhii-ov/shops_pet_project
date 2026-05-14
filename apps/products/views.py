# from django.db import transaction
# from django.db.models import F
# from rest_framework.decorators import action
# from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.users.permissions import IsAdmin
from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related(
        'category'
    ).all().order_by('id')
    
    serializer_class = ProductSerializer
    lookup_field = 'id'

    filterset_fields = ['name', 'slug', 'category']
    search_fields = ['name', 'slug', 'category__name']
    ordering_fields = ['created_at']

    def get_permissions(self):
        if self.action in [
            'create',
            'update',
            'partial_update',
            'destroy',
            'sell',
        ]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [AllowAny]

        return [
            permission()
            for permission in permission_classes
        ]
