from django.contrib import admin

from .models import Discount, Item, Order, OrderItem, Tax


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "currency", "description")
    list_filter = ("currency",)
    search_fields = ("name", "description")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "get_total_amount", "discount", "tax")
    list_filter = ("created_at", "discount", "tax")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "percent")
    search_fields = ("name",)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("name", "percent")
    search_fields = ("name",)
