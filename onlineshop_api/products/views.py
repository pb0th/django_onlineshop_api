
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, StockSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Product
from rest_framework import status
from rest_framework.response import Response

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def destroy(self, request, *args, **kwargs):
        """Override delete to deactivate the product instead of deleting."""
        product = self.get_object()
        product.is_active = False
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ProductStockViewSet(ModelViewSet):
    serializer_class = StockSerializer
    def get_queryset(self):
        """Filter stocks based on product ID from the URL."""
        product_id = self.kwargs['product_id']  # Use product_id from URL
        return Stock.objects.filter(product_id=product_id)
    def perform_create(self, serializer):
        """Associate the stock with the specified product."""
        product = Product.objects.get(pk=self.kwargs['product_id'])
        serializer.save(product=product) 
