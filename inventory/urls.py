# inventory/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("add/", views.ProductCreateView.as_view(), name="product_add"),
    path("export/", views.export_products_csv, name="product_export"),
    path("import/", views.import_products_csv, name="product_import"),
    path('purchases/', views.PurchaseListView.as_view(), name='purchase_list'),
    path('sales/', views.SaleListView.as_view(), name='sale_list'),
    path('accounting/', views.AccountingHomeView.as_view(), name='accounting_home'),
]