# filters.py

import django_filters
from .models import Stock

class StockFilter(django_filters.FilterSet):
    # Using icontains for case-insensitive substring matching
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Stock
        fields = ['product', 'name', 'quantity']
