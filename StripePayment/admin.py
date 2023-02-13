from django.contrib import admin
from .models import *


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price")
    list_display_links = ("id", "name")
    search_fields = ("id", "name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "promo", "count_item_ir_order")
    list_display_links = ("id",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("id", "percent", "currency")
    list_display_links = ("id",)

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("id", "percent", "inclusive")
    list_display_links = ("id",)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("id", "currency")
    list_display_links = ("id",)
