from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SellerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SellerSerializer

    
