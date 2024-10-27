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