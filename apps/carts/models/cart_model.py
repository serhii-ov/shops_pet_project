from decimal import Decimal
import uuid

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from apps.shops.models import Shop


class Cart(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',
        null=True,
        blank=True,
    )

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='carts',
    )

    # for anonymous users
    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'shop']),
            models.Index(fields=['session_key']),
        ]

    def __str__(self):
        if self.user:
            return f'Cart {self.id} - {self.user}'
        return f'Guest cart {self.id}'

    @property
    def total_price(self):
        """Calculate total money for the whole cart based on cart items.
        """
        return sum(
            (item.total_price for item in self.items.all()),
            Decimal('0.00')
        )
        
    @property
    def total_items(self):
        """Calculate total number of items in the cart.
        """
        return sum(item.quantity for item in self.items.all())
    
    def clean(self):
        if self.user and self.session_key:
            raise ValidationError(
                "Cart cannot have both user and session key."
            )
        if not self.user and not self.session_key:
            raise ValidationError(
                "Cart must have either a user or a session key."
            )
