from rest_framework import serializers


class OrderCreateSerializer(
    serializers.Serializer
):
    customer_name = serializers.CharField(
        max_length=255
    )
    customer_email = serializers.EmailField()
    customer_phone = serializers.CharField(
        max_length=50
    )
    customer_address = serializers.CharField()
    

# serializer = OrderCreateSerializer(data=request.data)
# serializer.is_valid(raise_exception=True)
# order = (
#     OrderService.create_order_from_cart(
#         cart=cart,
#         **serializer.validated_data,
#     )
# )