from apps.orders.permissions import IsOrderOwner


def test_is_order_owner_permission(user, another_user):

    permission = IsOrderOwner()

    class DummyRequest:
        pass

    request = DummyRequest()
    request.user = user

    class DummyOrder:
        pass

    order = DummyOrder()
    order.user = user

    assert permission.has_object_permission(
        request,
        None,
        order,
    )

    order.user = another_user

    assert not permission.has_object_permission(
        request,
        None,
        order,
    )
