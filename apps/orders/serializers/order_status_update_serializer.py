from rest_framework import serializers


class OrderStatusUpdateSerializer(
    serializers.Serializer
):
    status = serializers.ChoiceField(
        choices=[
            "paid",
            "shipped",
            "completed",
            "cancelled",
        ]
    )
    cancellation_reason = (
        serializers.CharField(
            required=False,
            allow_blank=True,
        )
    )
