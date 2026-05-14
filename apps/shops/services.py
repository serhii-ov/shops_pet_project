from rest_framework.exceptions import ValidationError

from .models import ShopRating


class ShopRatingService:

    @staticmethod
    def rate_shop(*, user, shop, rating):
        """
        Create or update customer rating for a shop.
        """

        if not user.groups.filter(name="Customer").exists():
            raise ValidationError(
                "Only customers can rate shops."
            )

        obj, _ = ShopRating.objects.update_or_create(
            shop=shop,
            customer=user,
            defaults={"rating": rating},
        )

        return obj
