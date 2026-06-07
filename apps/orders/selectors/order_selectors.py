from apps.orders.models import Order


def base_order_queryset():

    return (
        Order.objects
        .prefetch_related("items")
        .select_related(
            "user",
            "shop",
        )
    )


def get_order_with_items(order_id):

    return base_order_queryset().get(
        id=order_id
    )


def get_user_orders(user):

    return (
        base_order_queryset()
        .filter(user=user)
        .order_by("-created_at")
    )


# def get_order_with_items(order_id):

#     return (
#         Order.objects
#         .prefetch_related("items")
#         .select_related(
#             "user",
#             "shop",
#         )
#         .get(id=order_id)
#     )


# def get_user_orders(user):

#     return (
#         Order.objects
#         .filter(user=user)
#         .prefetch_related("items")
#         .select_related("shop")
#         .order_by("-created_at")
#     )
