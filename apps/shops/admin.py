from django.contrib import admin

from .models import Shop, ShopRating


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'average_rating']


@admin.register(ShopRating)
class ShopRatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'customer', 'rating']
