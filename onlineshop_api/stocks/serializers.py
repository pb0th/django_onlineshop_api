from rest_framework import serializers
from .models import Stock, StockMovement
from products.models import Product

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['id', 'quantity', 'movement_type', 'description']


class StockSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = Stock
        fields = ['id', 'name', 'quantity', 'stock_date', 'product']