from django.db import models, IntegrityError
from django.utils.timezone import now
from products.models import Product
# Create your models here.

# Stock model with many-to-one relationship with Product
class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stocks")
    name = models.CharField(max_length=100, null=False, blank=False)
    quantity = models.PositiveIntegerField()
    stocking_date = models.DateTimeField(default=now)  # Stocking date

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.quantity} units of {self.product.name}"

    class Meta:
        ordering = ['-stocking_date']
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def delete(self, *args, **kwargs):
        if self.movements.exists():
            raise IntegrityError("Cannot delete stock with existing stock movements.")
        super().delete(*args, **kwargs)

    

class StockMovement(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="movements")
    quantity = models.PositiveIntegerField()
    from_quantity = models.PositiveIntegerField()
    to_quantity = models.PositiveIntegerField()
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