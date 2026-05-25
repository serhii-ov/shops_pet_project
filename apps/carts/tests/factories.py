import factory
from decimal import Decimal
from django.contrib.auth import get_user_model

from apps.carts.models import Cart, CartItem
from apps.shops.models import Shop
from apps.products.models import Product
from apps.categories.models import Category
from apps.shop_products.models import ShopProduct

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(
        lambda n: f"user{n}@test.com"
    )


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(
        lambda n: f"Category {n}"
    )


class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop

    name = factory.Sequence(
        lambda n: f"Shop {n}"
    )


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(
        lambda n: f"Product {n}"
    )

    category = factory.SubFactory(
        CategoryFactory
    )


class ShopProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShopProduct

    shop = factory.SubFactory(
        ShopFactory
    )

    product = factory.SubFactory(
        ProductFactory
    )

    price = Decimal("10.00")
    stock = 20
    is_available = True


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(
        UserFactory
    )

    shop = factory.SubFactory(
        ShopFactory
    )


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(
        CartFactory
    )

    shop_product = factory.SubFactory(
        ShopProductFactory,
        shop=factory.SelfAttribute(
            "..cart.shop"
        ),
    )

    quantity = 2

    product_name = factory.LazyAttribute(
        lambda obj: obj.shop_product.product.name
    )

    price = Decimal("10.00")
