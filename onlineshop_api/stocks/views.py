from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import StockSerializer
from .models import Stock

# Create your views here.

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    
    

 