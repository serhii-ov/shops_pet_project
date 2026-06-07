from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.orders.models import Order


class OrderStatusService:

    @staticmethod
    @transaction.atomic
    def mark_as_paid(
        *,
        order: Order,
        payment_provider_id: str | None = None,
    ) -> Order:

        if order.status == Order.Status.CANCELLED:
            raise ValidationError(
                "Cancelled order cannot be paid."
            )

        if order.payment_status == Order.PaymentStatus.PAID:
            raise ValidationError(
                "Order is already paid."
            )

        order.status = Order.Status.PAID

        order.payment_status = (
            Order.PaymentStatus.PAID
        )

        order.payment_provider_id = (
            payment_provider_id
        )

        order.paid_at = timezone.now()

        order.save(
            update_fields=[
                "status",
                "payment_status",
                "payment_provider_id",
                "paid_at",
                "updated_at",
            ]
        )

        return order

    @staticmethod
    @transaction.atomic
    def mark_as_shipped(
        *,
        order: Order,
    ) -> Order:

        if order.status == Order.Status.CANCELLED:
            raise ValidationError(
                "Cancelled order cannot be shipped."
            )

        if order.payment_status != (
            Order.PaymentStatus.PAID
        ):
            raise ValidationError(
                "Order must be paid before shipping."
            )

        if order.shipment_status == (
            Order.ShipmentStatus.SHIPPED
        ):
            raise ValidationError(
                "Order is already shipped."
            )

        order.status = Order.Status.SHIPPED

        order.shipment_status = (
            Order.ShipmentStatus.SHIPPED
        )

        order.shipped_at = timezone.now()

        order.save(
            update_fields=[
                "status",
                "shipment_status",
                "shipped_at",
                "updated_at",
            ]
        )

        return order

    @staticmethod
    @transaction.atomic
    def mark_as_completed(
        *,
        order: Order,
    ) -> Order:

        if order.status == Order.Status.CANCELLED:
            raise ValidationError(
                "Cancelled order cannot be completed."
            )

        if order.shipment_status not in [
            Order.ShipmentStatus.SHIPPED,
            Order.ShipmentStatus.DELIVERED,
        ]:
            raise ValidationError(
                "Order must be shipped before completion."
            )

        if order.status == (
            Order.Status.COMPLETED
        ):
            raise ValidationError(
                "Order is already completed."
            )

        order.status = Order.Status.COMPLETED

        order.shipment_status = (
            Order.ShipmentStatus.DELIVERED
        )

        order.completed_at = timezone.now()

        order.save(
            update_fields=[
                "status",
                "shipment_status",
                "completed_at",
                "updated_at",
            ]
        )

        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(
        *,
        order: Order,
        reason: str,
    ) -> Order:

        if order.status == (
            Order.Status.COMPLETED
        ):
            raise ValidationError(
                "Completed order cannot be cancelled."
            )

        if order.status == (
            Order.Status.CANCELLED
        ):
            raise ValidationError(
                "Order is already cancelled."
            )

        order.status = Order.Status.CANCELLED

        order.cancellation_reason = reason

        # restore stock
        for item in order.items.select_related(
            "shop_product"
        ):
            if item.shop_product:
                item.shop_product.stock += (
                    item.quantity
                )
                item.shop_product.save(
                    update_fields=["stock"]
                )

        order.save(
            update_fields=[
                "status",
                "cancellation_reason",
                "updated_at",
            ]
        )

        return order
