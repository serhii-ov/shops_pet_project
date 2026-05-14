from django.db import models


class CartItem(models.Model):
    cart = models.ForeignKey(
        'cart.Cart',
        on_delete=models.CASCADE,
        related_name='items',
    )

    shop_product = models.ForeignKey(
        'shops.ShopProduct',
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'shop_product')

    def __str__(self):
        return f'{self.shop_product} x {self.quantity}'
