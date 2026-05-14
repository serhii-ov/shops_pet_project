import pytest

from django.contrib.auth.models import Group
from rest_framework.exceptions import ValidationError

from apps.shops.models import Shop, ShopRating
from apps.shops.services import ShopRatingService


@pytest.mark.django_db
class TestShopRatingService:

    def test_customer_can_rate_shop(self, django_user_model):
        customer_group, _ = Group.objects.get_or_create(
            name="Customer"
        )

        user = django_user_model.objects.create_user(
            email="customer@example.com",
            password="pass123"
        )

        user.groups.add(customer_group)

        shop = Shop.objects.create(name="Shop 1")

        rating = ShopRatingService.rate_shop(
            user=user,
            shop=shop,
            rating=5,
        )

        assert isinstance(rating, ShopRating)
        assert rating.rating == 5

    def test_non_customer_cannot_rate_shop(
        self,
        django_user_model
    ):
        customer_group, _ = Group.objects.get_or_create(
            name="Customer"
        )

        user = django_user_model.objects.create_user(
            email="regular_user@example.com",
            password="pass123"
        )

        # ensure user is NOT a customer
        user.groups.remove(customer_group)

        shop = Shop.objects.create(name="Shop 1")

        with pytest.raises(ValidationError):
            ShopRatingService.rate_shop(
                user=user,
                shop=shop,
                rating=4,
            )

    def test_existing_rating_is_updated(
        self,
        django_user_model
    ):
        customer_group, _ = Group.objects.get_or_create(
            name="Customer"
        )

        user = django_user_model.objects.create_user(
            email="customer2@example.com",
            password="pass123"
        )

        user.groups.add(customer_group)

        shop = Shop.objects.create(name="Shop 1")

        ShopRating.objects.create(
            shop=shop,
            customer=user,
            rating=2
        )

        updated_rating = ShopRatingService.rate_shop(
            user=user,
            shop=shop,
            rating=5,
        )

        assert ShopRating.objects.count() == 1
        assert updated_rating.rating == 5
