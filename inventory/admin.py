
from django.contrib import admin
from .models import Product, Bill, BillItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "quantity", "category")
    search_fields = ("name", "category")
    list_filter = ("category",)


class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1
    readonly_fields = ("price",)


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "created_at", "total_amount")
    search_fields = ("customer_name",)
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "total_amount")
    inlines = [BillItemInline]


@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ("id", "bill", "product", "quantity", "price")
    list_filter = ("product",)
