import pytest
from django.contrib.auth import get_user_model

from apps.shops.models import Shop, ShopRating

User = get_user_model()


@pytest.mark.django_db
class TestShopModels:

    def test_shop_rating_updates_average_rating(self):
        shop = Shop.objects.create(name="Test Shop")

        user1 = User.objects.create_user(
            email="customer1@example.com",
            password="pass123"
        )
        user2 = User.objects.create_user(
            email="customer2@example.com",
            password="pass123"
        )

        ShopRating.objects.create(
            shop=shop,
            customer=user1,
            rating=4
        )

        shop.refresh_from_db()
        assert shop.average_rating == 4.0

        ShopRating.objects.create(
            shop=shop,
            customer=user2,
            rating=2
        )

        shop.refresh_from_db()
        assert shop.average_rating == 3.0

    def test_delete_rating_updates_average_rating(self):
        shop = Shop.objects.create(name="Test Shop")

        user = User.objects.create_user(
            email="customer@example.com",
            password="pass123"
        )

        rating = ShopRating.objects.create(
            shop=shop,
            customer=user,
            rating=5
        )

        shop.refresh_from_db()
        assert shop.average_rating == 5.0

        rating.delete()

        shop.refresh_from_db()
        assert shop.average_rating == 0

    def test_unique_rating_per_customer_and_shop(self):
        shop = Shop.objects.create(name="Test Shop")

        user = User.objects.create_user(
            email="customer@example.com",
            password="pass123"
        )

        ShopRating.objects.create(
            shop=shop,
            customer=user,
            rating=5
        )

        with pytest.raises(Exception):
            ShopRating.objects.create(
                shop=shop,
                customer=user,
                rating=3
            )
