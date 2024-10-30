from .views import StockViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include



router = DefaultRouter()
router.register(r'', StockViewSet, basename='stock')

urlpatterns = [
    path('', include(router.urls)),
]
