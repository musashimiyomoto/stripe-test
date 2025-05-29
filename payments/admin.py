from django.contrib import admin

from .models import Discount, Item, Order, OrderItem, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "currency")
    list_filter = ("currency",)
    search_fields = ("name", "description")


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "percent", "min_order_amount", "min_items_count", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    fieldsets = (
        (None, {
            'fields': ('name', 'percent', 'is_active')
        }),
        ('Условия применения', {
            'fields': ('min_order_amount', 'min_items_count'),
            'description': 'Скидка будет применена только если выполнены все указанные условия'
        }),
    )


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ("name", "percent", "currency", "is_default", "is_active")
    list_filter = ("currency", "is_default", "is_active")
    search_fields = ("name",)
    fieldsets = (
        (None, {
            'fields': ('name', 'percent', 'is_active')
        }),
        ('Условия применения', {
            'fields': ('currency', 'is_default'),
            'description': 'Налог будет применен автоматически на основе валюты заказа'
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "get_total_amount", "discount", "tax", "session_key")
    list_filter = ("created_at", "discount", "tax")
    search_fields = ("id", "session_key")
    inlines = [OrderItemInline]
    readonly_fields = ("session_key", "created_at", "get_total_amount")
    
    fieldsets = (
        (None, {
            'fields': ('session_key', 'created_at')
        }),
        ('Налоги и скидки', {
            'fields': ('discount', 'tax'),
            'description': 'Налоги и скидки применяются автоматически при оплате'
        }),
        ('Итого', {
            'fields': ('get_total_amount',)
        }),
    )
