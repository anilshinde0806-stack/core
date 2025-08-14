from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),


]
