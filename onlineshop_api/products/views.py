
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer
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




