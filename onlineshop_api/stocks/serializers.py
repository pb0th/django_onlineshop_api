from rest_framework import serializers
from .models import Stock, StockMovement
from products.models import Product

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['id', 'quantity', 'from_quantity', 'to_quantity', 'movement_type', 'description', 'stock']
        read_only_fields = ['from_quantity', 'to_quantity'] 
        
    
    def validate(self, attrs):
        stock = attrs['stock']
        movement_type = attrs['movement_type']
        quantity = attrs['quantity']

        if movement_type == 'OUT' and stock.quantity < quantity:
            raise serializers.ValidationError(
                {"quantity": "Insufficient stock for this operation."}
            )

        return attrs

    def save(self,  **kwargs):
        movement_type = self.validated_data['movement_type']
        quantity = self.validated_data['quantity']
        stock = self.validated_data['stock']
        from_quantity = stock.quantity

        if movement_type == "IN":
            to_quantity = from_quantity + quantity
        elif movement_type == "OUT":
            to_quantity = from_quantity - quantity
        
        new_stock_movement = StockMovement.objects.create(
            stock=stock,
            quantity=quantity,
            from_quantity=from_quantity,
            to_quantity=to_quantity,
            movement_type=movement_type,
            description=self.validated_data.get('description', '')
        )

        stock.quantity = to_quantity
        stock.save()

        return new_stock_movement



class StockSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = Stock
        fields = ['id', 'name', 'quantity', 'stocking_date', 'product']
        # read_only_fields = ['quantity', 'product']

    def validate(self, attrs):
        if self.instance:
            if 'quantity' in attrs:
                raise serializers.ValidationError({"quantity": "Quantity cannot be updated."})
            if 'product' in attrs:
                raise serializers.ValidationError({"product": "Product cannot be updated."})
        return attrs

    def update(self, instance, validated_data):
        """Proceed with updates if valid."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

