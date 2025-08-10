from rest_framework import viewsets
from core.models import Booking
from core.models import  Product
from .serializers import BookingSerializer, ProductSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
from django.shortcuts import render

# Create your views here.
