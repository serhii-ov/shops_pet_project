from django.db import models
from apps.shops.models import Shop


class ShopProduct(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='shop_products'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='product_shops'
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('shop', 'product')

    def __str__(self):
        return f'{self.shop} -> {self.product}'
