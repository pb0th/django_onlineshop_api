from rest_framework import serializers
from categories.models import Category

# from products.models import Product


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'retail_price', 'is_active']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']