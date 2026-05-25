from apps.carts.models.cart_model import Cart
from apps.carts.services.cart_service import CartService


class CartMixin:

    def get_session_key(self):
        request = self.request

        if not request.session.session_key:
            request.session.create()
            
        return request.session.session_key

    def get_cart(self, shop):

        return CartService.get_or_create_cart(
            user=self.request.user,
            session_key=self.get_session_key(),
            shop=shop,
        )
