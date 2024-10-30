# filters.py

import django_filters
from .models import Product



class ProductFilter(django_filters.FilterSet):
    # Filter for name with case-insensitive substring matching
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    
    # Filters for retail_price with greater than or equal to (gte) and less than or equal to (lte)
    retail_price_gte = django_filters.NumberFilter(field_name='retail_price', lookup_expr='gte')
    retail_price_lte = django_filters.NumberFilter(field_name='retail_price', lookup_expr='lte')
    
    # Filters for cost_price with greater than or equal to (gte) and less than or equal to (lte)
    cost_price_gte = django_filters.NumberFilter(field_name='cost_price', lookup_expr='gte')
    cost_price_lte = django_filters.NumberFilter(field_name='cost_price', lookup_expr='lte')
    
    class Meta:
        model = Product
        fields = ['categories', 'is_active'] 
