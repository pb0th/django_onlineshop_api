from rest_framework import serializers
from .models import Product
from categories.models import Category


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset= Category.objects.all())
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'retail_price', 'cost_price', 'image',
            'is_active', 'categories', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        if not attrs['categories']:
            raise serializers.ValidationError({'categories':'at least one category is required.'})
        return super().validate(attrs)