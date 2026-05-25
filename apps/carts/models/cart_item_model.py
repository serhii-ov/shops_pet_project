from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from .cart_model import Cart
from apps.shop_products.models import ShopProduct


class CartItem(models.Model):
    """
    Snapshot of product information at the moment
    it was added to cart.
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
    )

    shop_product = models.ForeignKey(
        ShopProduct,
        on_delete=models.CASCADE,
        related_name='cart_items',
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        default=1,
    )

    # snapshot fields
    product_name = models.CharField(
    max_length=255,
    blank=True,
    null=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'shop_product')
        ordering = ['created_at']

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'

    @property
    def total_price(self):
        """Calculate total price for one item based on quantity and price.
        """
        return self.price * Decimal(self.quantity)

    def save(self, *args, **kwargs):
        """
        Save snapshot data automatically.
        """
        if not self.product_name:
            self.product_name = self.shop_product.product.name

        if self.price is None:
            self.price = self.shop_product.price

        self.full_clean()

        super().save(*args, **kwargs)

    def clean(self):
        if self.shop_product.shop_id != self.cart.shop_id:
            raise ValidationError(
                "Cart item shop must match cart shop."
            )
