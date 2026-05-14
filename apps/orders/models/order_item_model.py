from django.db import models


class OrderItem(models.Model):
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='items',
    )

    shop_product = models.ForeignKey(
        'shops.ShopProduct',
        on_delete=models.CASCADE,
        related_name='order_items',
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f'{self.shop_product} x {self.quantity}'
