from django.contrib import admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    BillingAddress,
    ShippingAddress,
    Order,
    OrderItem,
)


# Register your models here.


# ========== Inline ==========
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    verbose_name = _("Order Item")
    verbose_name_plural = _("Order Items")
# ========== END Inline ==========


@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "company_name", "address", "city", "country", "email", "phone_number", "created_at", "updated_at"]


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "company_name", "address", "city", "country", "email", "phone_number", "created_at", "updated_at"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ["id", "user", "billing_address", "shipping_address", "ordered_date", "is_paid", "created_at", "updated_at"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product_version", "quantity", "price", "created_at", "updated_at"]