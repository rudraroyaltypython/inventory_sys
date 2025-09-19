# inventory/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
    Product, Category,
    Supplier, Purchase, PurchaseItem,
    Customer, Sale, SaleItem
)


# -----------------------
# Inline Admins
# -----------------------
class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1   # show 1 empty row by default


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1


# -----------------------
# Product Admin (with import/export)
# -----------------------
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ("name", "sku", "category", "unit_price", "tax_percent", "stock")


# -----------------------
# Category Admin
# -----------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


# -----------------------
# Supplier Admin
# -----------------------
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "email")


# -----------------------
# Customer Admin
# -----------------------
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "contact", "email")


# -----------------------
# Purchase Admin (with inline items)
# -----------------------
@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("id", "supplier", "date", "total_amount")
    inlines = [PurchaseItemInline]


# -----------------------
# Sale Admin (with inline items)
# -----------------------
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "date", "total_amount")
    inlines = [SaleItemInline]
