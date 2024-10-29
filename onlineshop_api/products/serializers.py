from rest_framework import serializers
from .models import Product
from categories.models import Category
from categories.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        many=True,
        write_only=True
    )
    category_details = CategorySerializer(many=True, read_only=True, source='categories')
    # Add a default value for 'is_active'
    is_active = serializers.BooleanField(default=True)
    class Meta:
        model = Product
        fields = [
            'id', 
            'name', 
            'description', 
            'retail_price', 
            'cost_price', 
            'image', 
            'is_active', 
            'categories', 
            'category_details',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    def validate_categories(self, value):
        """Ensure categories are not an empty array."""
        if not value:
            raise serializers.ValidationError("Categories cannot be empty.")
        return value

    def validate(self, attrs):
        """Handle different validation logic for create and update."""
        # Check if it's a create operation
        if self.instance is None:
            # On create, ensure categories are provided
            if 'categories' not in attrs:
                raise serializers.ValidationError({
                    'categories': 'This field is required.'
                })
        else:
            # On update, check if categories exist and ensure it's non-empty
            if 'categories' in attrs and not attrs['categories']:
                raise serializers.ValidationError({
                    'categories': 'This field cannot be empty.'
                })

        return super().validate(attrs)