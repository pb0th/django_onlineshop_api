from django.db import models
from django.utils.timezone import now 

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Active: {'Yes' if self.is_active else 'No'})"
    class Meta:
        ordering = ['created_at']
        verbose_name = "Category"
        verbose_name_plural = "Categories"