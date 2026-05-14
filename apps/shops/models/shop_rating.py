from django.conf import settings
from django.db import models
from django.core.validators import (
    MinValueValidator, 
    MaxValueValidator,
    )

from .shop import Shop


class ShopRating(models.Model):
    shop = models.ForeignKey(
        Shop,
        related_name='ratings',
        on_delete=models.CASCADE
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='shop_ratings',
        on_delete=models.CASCADE
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('shop', 'customer')

    def __str__(self):
        return f'{self.customer} -> {self.shop} ({self.rating})'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.shop.update_rating()

    def delete(self, *args, **kwargs):
        shop = self.shop
        super().delete(*args, **kwargs)
        shop.update_rating()
