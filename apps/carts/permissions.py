from rest_framework.permissions import BasePermission


class IsCartOwner(BasePermission):

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        if request.user.is_authenticated:
            return obj.cart.user == request.user

        return (
            obj.cart.session_key ==
            request.session.session_key
        )
