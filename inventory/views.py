import csv
from decimal import Decimal, InvalidOperation

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Product, Category, Purchase, Sale


# -----------------------
# Product Views
# -----------------------
class ProductListView(ListView):
    model = Product
    template_name = "inventory/product_list.html"
    context_object_name = "products"


class ProductCreateView(CreateView):
    model = Product
    fields = ["sku", "name", "category", "unit_price", "tax_percent", "stock"]
    template_name = "inventory/product_form.html"
    success_url = reverse_lazy("product_list")


def export_products_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(["SKU", "Name", "Category", "Unit Price", "Tax %", "Stock"])

    for product in Product.objects.all():
        writer.writerow([
            product.sku,
            product.name,
            product.category.name if product.category else "",
            product.unit_price,
            product.tax_percent,
            product.stock,
        ])

    return response


def import_products_csv(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        count = 0
        for row in reader:
            try:
                category_name = row.get("Category", "").strip()
                category = None
                if category_name:
                    category, _ = Category.objects.get_or_create(name=category_name)

                # safely convert to numbers
                try:
                    unit_price = Decimal(row.get("Unit Price") or 0)
                except InvalidOperation:
                    unit_price = Decimal(0)

                try:
                    tax_percent = Decimal(row.get("Tax %") or 0)
                except InvalidOperation:
                    tax_percent = Decimal(0)

                try:
                    stock = Decimal(row.get("Stock") or 0)
                except InvalidOperation:
                    stock = Decimal(0)

                Product.objects.update_or_create(
                    sku=row["SKU"].strip(),
                    defaults={
                        "name": row.get("Name", "").strip(),
                        "category": category,
                        "unit_price": unit_price,
                        "tax_percent": tax_percent,
                        "stock": stock,
                    },
                )
                count += 1

            except Exception as e:
                messages.error(request, f"Error importing row {row}: {e}")

        messages.success(request, f"{count} products imported successfully!")
        return redirect("product_list")

    return render(request, "inventory/product_import.html")


# -----------------------
# Purchase Views
# -----------------------
class PurchaseListView(ListView):
    model = Purchase
    template_name = "inventory/purchase_list.html"
    context_object_name = "purchases"


# -----------------------
# Sale Views
# -----------------------
class SaleListView(ListView):
    model = Sale
    template_name = "inventory/sale_list.html"
    context_object_name = "sales"


# -----------------------
# Accounting Home
# -----------------------
class AccountingHomeView(TemplateView):
    template_name = "inventory/accounting_home.html"
