from django.utils import timezone
import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from apps.shops.models import Shop


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    class ShipmentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        IN_TRANSIT = "in_transit", "In Transit"
        DELIVERED = "delivered", "Delivered"
        RETURNED = "returned", "Returned"

    class PaymentMethod(models.TextChoices):
        CARD = "card", "Card"
        CASH = "cash", "Cash"
        PAYPAL = "paypal", "PayPal"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    order_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    # tracks the fulfillment or operational state of the order
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    # tracks the financial state of the order
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    payment_provider_id = models.CharField(
        max_length=255,
        blank=True,
    )
    shipment_status = models.CharField(
        max_length=20,
        choices=ShipmentStatus.choices,
        default=ShipmentStatus.PENDING,
    )
    delivery_notes = models.TextField(
        blank=True,
    )
    cancellation_reason = models.TextField(
        blank=True,
    )

    customer_name = models.CharField(
        max_length=255,
    )
    customer_email = models.EmailField()
    customer_phone = models.CharField(
        max_length=50,
    )
    customer_address = models.TextField()

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    shipped_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    cancelled_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CARD,
    )
    
    tracking_number = models.CharField(
        max_length=255,
        blank=True,
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
    )
    total_items = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )

    shipping_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
    )
    tax_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
    )
    discount_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
    )
    
    # Final Total (Calculated at checkout)
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=Decimal("0.00")
    )

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(total_price__gte=0),
                name="order_total_price_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(total_items__gte=0),
                name="order_total_items_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(total__gte=0),
                name="order_total_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(shipping_cost__gte=0),
                name="order_shipping_cost_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(tax_amount__gte=0),
                name="order_tax_amount_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(discount_amount__gte=0),
                name="order_discount_amount_gte_zero",
            ),
        ]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["shipment_status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["shop"]),
            models.Index(fields=["shop", "status"]),
            models.Index(fields=["shop", "-created_at"]),
            models.Index(fields=["order_number"]),
        ]

    def __str__(self):
        return self.order_number
    
    def clean(self):
        if (
            self.status == self.Status.COMPLETED
            and self.payment_status != self.PaymentStatus.PAID
        ):
            raise ValidationError(
                "Completed order must be paid."
            )
        
        if (
            self.shipment_status in [
                self.ShipmentStatus.SHIPPED,
                self.ShipmentStatus.IN_TRANSIT,
                self.ShipmentStatus.DELIVERED,
            ]
            and self.payment_status != self.PaymentStatus.PAID
        ): 
            raise ValidationError(
                "Shipped order must be paid."
            )
        if (
            self.shipment_status == self.ShipmentStatus.DELIVERED
            and self.status != self.Status.COMPLETED
        ):
            raise ValidationError(
                "Delivered order should be completed."
            )
        if (
            self.status == self.Status.CANCELLED
            and not self.cancellation_reason
        ):
            raise ValidationError(
                "Cancelled orders require a reason."
            )
        if (
            self.status == self.Status.PAID
            and self.payment_status != self.PaymentStatus.PAID
        ):
            raise ValidationError(
                "Paid orders must have paid payment status."
            )

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = (
                f"ORD-{timezone.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}"
            )

        self.total = self.total_price + self.shipping_cost + self.tax_amount - self.discount_amount
        if self.total < 0:
            raise ValidationError(
                "Order total cannot be negative."
            )
        
        self.full_clean()
        super().save(*args, **kwargs)
