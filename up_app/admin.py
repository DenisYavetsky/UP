from django.contrib import admin
from .models import *


class CartTabularInline(admin.TabularInline):
    model = Cart


class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [CartTabularInline]


admin.site.register(Collection)
admin.site.register(Product)
admin.site.register(Cost)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatus)
admin.site.register(Delivery)


