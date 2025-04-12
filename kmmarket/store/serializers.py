from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryForProduct(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    # category = CategoryForProduct()
    class Meta:
        model = Product
        fields = '__all__'
        depth = 1
        read_only_fields=['image']

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'