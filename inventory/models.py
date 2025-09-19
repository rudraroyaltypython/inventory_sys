from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# -----------------------
# Supplier
# -----------------------
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# -----------------------
# Purchase
# -----------------------
class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Purchase {self.id} - {self.supplier.name}"


# -----------------------
# Purchase Item
# -----------------------
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", related_name="purchase_items", on_delete=models.CASCADE)  # fixed
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    

# -----------------------
# Customer
# -----------------------
class Customer(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# -----------------------
# Sale
# -----------------------
class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Sale {self.id}"
    

# -----------------------
# Sale Item
# -----------------------
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", related_name="sale_items", on_delete=models.CASCADE)  # fixed
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    

# -----------------------
# Signals to update stock
# -----------------------
@receiver(post_save, sender=PurchaseItem)
def increase_stock(sender, instance, created, **kwargs):
    if created:  # only when new PurchaseItem is added
        instance.product.stock += instance.quantity
        instance.product.save()


@receiver(post_save, sender=SaleItem)
def decrease_stock(sender, instance, created, **kwargs):
    if created:  # only when new SaleItem is added
        instance.product.stock -= instance.quantity
        instance.product.save()


# -----------------------
# Category
# -----------------------
class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# -----------------------
# Product
# -----------------------
class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)  # purchase or sale base price
    tax_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # quantity on hand

    def __str__(self):
        return f"{self.name} ({self.sku})"
