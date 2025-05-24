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
    # This is write-only: accepts category ID on write
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )

    # This is read-only: returns category object on read
    category_data = CategoryForProduct(read_only=True, source='category')

    class Meta:
        model = Product
        fields = '__all__'  # or list all fields manually
        # If you use '__all__', make sure 'category_data' is added dynamically

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request', None)

        if request and request.method in ['POST', 'PUT', 'PATCH']:
            # On write: remove category_data (no nested object)
            self.fields.pop('category_data', None)
        else:
            # On read: remove the write-only category ID field
            self.fields.pop('category', None)

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
        

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        depth = 1

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'
class TrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')


        if request and request.method == 'GET':
            # Add nested client user username
            rep['client'] = {
                'id': instance.client.id,
                'user': {
                    'id': instance.client.user.id,
                    'username': instance.client.user.username
                }
            }


            # Serialize products with nested data
            rep['products'] = ProductSerializer(instance.products, many=False).data

        return rep