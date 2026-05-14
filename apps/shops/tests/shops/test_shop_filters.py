import pytest


@pytest.mark.django_db
class TestShopRatingFilters:

    def test_filter_by_exact_rating(self, api_client, shops):
        response = api_client.get('/shops/', {
            'average_rating': 4.0
        })
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Shop 2'

    def test_filter_by_rating_gte(self, api_client, shops):
        response = api_client.get('/shops/', {
            'average_rating__gte': 4.0
        })
        assert response.status_code == 200
        assert len(response.data['results']) == 2

        ratings = [shop['average_rating'] for shop in response.data['results']]
        assert all(rating >= 4.0 for rating in ratings)

    def test_filter_by_rating_lte(self, api_client, shops):
        response = api_client.get('/shops/', {
            'average_rating__lte': 4.0
        })
        assert response.status_code == 200
        assert len(response.data['results']) == 2

        ratings = [shop['average_rating'] for shop in response.data['results']]
        assert all(rating <= 4.0 for rating in ratings)

    def test_filter_by_rating_gt(self, api_client, shops):
        response = api_client.get('/shops/', {
            'average_rating__gt': 4.0
        })
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Shop 3'

    def test_filter_by_rating_lt(self, api_client, shops):
        response = api_client.get('/shops/', {
            'average_rating__lt': 4.0
        })
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['name'] == 'Shop 1'
