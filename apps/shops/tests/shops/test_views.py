import pytest

from apps.shops.models import Shop, ShopRating


@pytest.mark.django_db
class TestShopViews:

    def test_list_shops(self, api_client):
        Shop.objects.create(name="Shop A")
        Shop.objects.create(name="Shop B")

        response = api_client.get("/shops/")

        assert response.status_code == 200
        assert response.data["count"] == 2
        assert len(response.data["results"]) == 2

    def test_admin_can_create_shop(
        self,
        api_client,
        admin_user
    ):
        api_client.force_authenticate(user=admin_user)

        payload = {
            "name": "New Shop",
            "address": "Address 1"
        }

        response = api_client.post("/shops/", payload)

        assert response.status_code == 201
        assert Shop.objects.count() == 1

    def test_customer_cannot_create_shop(
        self,
        api_client,
        customer_user
    ):
        api_client.force_authenticate(user=customer_user)

        payload = {
            "name": "New Shop",
            "address": "Address 1"
        }

        response = api_client.post("/shops/", payload)

        assert response.status_code == 403

    def test_customer_can_rate_shop(
        self,
        api_client,
        customer_user
    ):
        api_client.force_authenticate(user=customer_user)

        shop = Shop.objects.create(name="Shop A")

        payload = {
            "shop": shop.id,
            "rating": 5
        }

        response = api_client.post(
            "/shops/rate/",
            payload
        )

        assert response.status_code == 201
        assert ShopRating.objects.count() == 1

    def test_customer_rating_history(
        self,
        api_client,
        customer_user
    ):
        api_client.force_authenticate(user=customer_user)

        shop = Shop.objects.create(name="Shop A")

        ShopRating.objects.create(
            shop=shop,
            customer=customer_user,
            rating=4
        )

        response = api_client.get(
            "/shops/my-ratings/"
        )

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1

    def test_shop_search(self, api_client):
        Shop.objects.create(name="Coffee Shop")
        Shop.objects.create(name="Book Store")

        response = api_client.get(
            "/shops/?search=Coffee"
        )

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Coffee Shop"

    def test_shop_ordering(self, api_client):
        Shop.objects.create(
            name="Shop A",
            average_rating=3
        )

        Shop.objects.create(
            name="Shop B",
            average_rating=5
        )

        response = api_client.get(
            "/shops/?ordering=-average_rating"
        )

        assert response.status_code == 200
        assert response.data["results"][0]["name"] == "Shop B"
        