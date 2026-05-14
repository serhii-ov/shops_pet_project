from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.users.permissions import IsCustomer

from apps.shops.models import ShopRating
from apps.shops.serializers import ShopRatingSerializer
from apps.shops.services import ShopRatingService


class ShopRatingCreateView(generics.CreateAPIView):
    queryset = ShopRating.objects.all()
    serializer_class = ShopRatingSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rating = ShopRatingService.rate_shop(
            user=request.user,
            shop=serializer.validated_data["shop"],
            rating=serializer.validated_data["rating"],
        )

        response_serializer = self.get_serializer(rating)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class CustomerRatingHistoryView(generics.ListAPIView):
    serializer_class = ShopRatingSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return ShopRating.objects.filter(
            customer=self.request.user
        ).select_related('shop').order_by('-created_at')
