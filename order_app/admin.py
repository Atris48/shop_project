from django.contrib import admin
from . import models


class FactorItemAdmin(admin.TabularInline):
    model = models.FactorItem


@admin.register(models.Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'created_at']
    list_filter = ['user', ]
    inlines = [FactorItemAdmin, ]


class OrderItemAdmin(admin.TabularInline):
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_price', 'tracking_code', 'created_at']
    list_filter = ['user', 'created_at', 'order_status']
    search_fields = ['tracking_code', 'year']
    inlines = [OrderItemAdmin, ]


@admin.register(models.FactorDiscount)
class FactorDiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'percentage', 'expiration_time']
    list_filter = ['expiration_time', ]


admin.site.register(models.OrderReferral)
