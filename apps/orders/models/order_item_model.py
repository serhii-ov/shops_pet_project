from decimal import Decimal
from djmoney.models.fields import MoneyField


from django.core.validators import MinValueValidator
from django.db import models

from apps.orders.models.order_model import Order
from apps.shop_products.models import ShopProduct


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    shop_product = models.ForeignKey(
        ShopProduct,
        on_delete=models.PROTECT,
        null=False,
        related_name="order_items",
    )
        
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    # snapshot product data
    product_name = models.CharField(
        max_length=255,
    )
    product_sku = models.CharField(
        max_length=100,
        blank=True,
    )
    product_description = models.TextField(
        blank=True,
    )
 
    price = MoneyField(
        max_digits=10, 
        decimal_places=2, 
        default_currency='USD',
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["order", "shop_product"],
                name="unique_product_per_order",
            ),
            models.CheckConstraint(
            condition=models.Q(quantity__gte=1),
            name="orderitem_quantity_gt_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=0), 
                name="orderitem_price_gte_zero",
            )
        ]
        
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["shop_product"]),
        ]

    @property
    def total_price(self):
        return self.price * Decimal(self.quantity)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
