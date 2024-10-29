from django.db import models
from django.utils.timezone import now
from categories.models import Category
from shared.utils.generate_file_upload_path import generate_file_upload_path





# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    image = models.ImageField(upload_to=generate_file_upload_path, max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name="products")

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name} (Active: {'Yes' if self.is_active else 'No'})"
    class Meta:
        ordering = ['created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"



# Stock model with many-to-one relationship with Product
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    name = models.CharField(max_length=100, null=False, blank=False)
    quantity = models.PositiveIntegerField()
    stocking_date = models.DateField(default=now)  # Stocking date

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.quantity} units of {self.product.name}"

    class Meta:
        ordering = ['-stocking_date']
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

class StockMovement(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="movements")
    quantity = models.PositiveIntegerField()
    MOVEMENT_CHOICES = (
        ('IN', 'Stock In'),   # Restocking
        ('OUT', 'Stock Out'), # Sale or usage
    )
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_CHOICES)
    description = models.CharField(max_length=255, blank=True, null=True)  # Optional description
    
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.movement_type} - {self.stock.product.name} ({self.quantity})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"
