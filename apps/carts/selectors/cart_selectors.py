"""
What belongs in selectors?
Read/query logic:
optimized prefetches
filtering
cart retrieval
analytics queries
"""
from apps.carts.models import Cart


def get_cart_with_items(cart_id):

    return (
        Cart.objects
        .prefetch_related(
            'items',
            'items__shop_product',
            'items__shop_product__product',
            'items__shop_product__shop',
        )
        .get(id=cart_id)
    )
