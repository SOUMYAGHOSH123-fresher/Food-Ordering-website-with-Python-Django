from django.contrib import admin
from .models import Category, Items, Cart, CartItem, Order, OrderItem


class ItemAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    ordering = ['item_name']
    list_per_page = 10

# Register your models here.
admin.site.register(Category)
admin.site.register(Items, ItemAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)