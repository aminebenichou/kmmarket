from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token

# Create your views here.

def createUser(data):
    try:
        user = User.objects.create_user(**data)
        token = Token.objects.create(user=user)
        return {"message":"User created Successfully", "status":201}
    except NameError:
        return {"message":f"Error : {NameError}", "status":400}
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        response = createUser(request.data)
        return Response(response, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def getUserInfo(request):
    print(request.user.id)
    snippets = User.objects.get(id=request.user.id)
    serializer = UserSerializer(snippets)
    return Response(serializer.data)