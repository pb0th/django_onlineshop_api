from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import StockSerializer
from .models import Stock
from django_filters.rest_framework import DjangoFilterBackend
from .filters import StockFilter

# Create your views here.

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter 

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Check for existing stock movements
        if instance.movements.exists():  # Assuming `movements` is the related name for stock movements
            return Response(
                {"detail": "Cannot delete stock with existing stock movements."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If no movements exist, call the parent destroy method to proceed with deletion
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

 