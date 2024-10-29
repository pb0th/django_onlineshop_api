from .views import ProductViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path, include

# Initialize a router and register the ProductViewSet
router = DefaultRouter()
router.register(r'', ProductViewSet, basename='product')


# Include the router's URLs in the urlpatterns list
urlpatterns = [
    path('', include(router.urls)),
]