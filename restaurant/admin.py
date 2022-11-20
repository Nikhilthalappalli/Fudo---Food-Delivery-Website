from django.contrib import admin

from restaurant.models import Cart, Cart_item, Menu, Restaurants

# Register your models here.

admin.site.register(Restaurants)
admin.site.register(Menu)
admin.site.register(Cart)
admin.site.register(Cart_item)