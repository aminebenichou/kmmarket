from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import api_view, action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
# Create your views here.

def createUser(data):
    try:
        user = User.objects.create_user(**data)
        token = Token.objects.create(user=user)
        return {"message":"User created Successfully", "status":201, 'userId':user.id}
    except NameError:
        return {"message":f"Error : {NameError}", "status":400}
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            print(self.request.data)
            seller = Seller.objects.get(user=self.request.user)
            category = Category.objects.get(id=int(self.request.data['category']))
            title = self.request.data['title']
            description = self.request.data['description']
            price = int(self.request.data['price'])
            self.queryset.create(title=title, price=price, description=description, seller=seller, category=category)
            return Response({'message': 'created successfully'}, status=status.HTTP_201_CREATED)
        except NameError:
            print(NameError)
            return Response({'message': NameError}, status=status.HTTP_502_BAD_GATEWAY)    
    
    @action(detail=False, methods=['get'], url_path='products-for-seller')
    def list_for_seller(self, request):
        user = request.user
        try:
            seller = user.seller
        except AttributeError:
            return Response({"error": "Authenticated user is not a seller."}, status=status.HTTP_403_FORBIDDEN)

        products = Product.objects.filter(seller=seller)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

    def create(self, request, *args, **kwargs):
        user_id = createUser(request.data)
        user = User.objects.get(id=user_id['userId'])
        # print(user['userId'])
        Seller.objects.create(user=user)
        return Response({"message":"seller created"})

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def create(self, request, *args, **kwargs):
        user_id = createUser(request.data)
        user = User.objects.get(id=user_id['userId'])
        print(user)
        Client.objects.create(user=user)
        return Response({"message":"Client created"})




class RatingViewSet(viewsets.ModelViewSet):
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer

class TrackingViewSet(viewsets.ModelViewSet):
    queryset = Tracking.objects.all()
    serializer_class = TrackingSerializer

    @action(detail=False, methods=['get'], url_path='by-order')
    def get_by_order_number(self, request):
        tracking_number = request.GET.get('tracking')
        if not tracking_number:
            return Response({'error': 'Tracking number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(order_number=tracking_number)
            tracking = Tracking.objects.get(order=order)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_204_NO_CONTENT)
        except Tracking.DoesNotExist:
            return Response({'error': 'Tracking info not found'}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(tracking)
        return Response(serializer.data)


# @api_view(['GET'])
# def getTracking(request):
#     tracking_number = request.GET.get('tracking')  # Use .get() instead of calling the dict
#     if not tracking_number:
#         return Response({'error': 'Tracking number is required'}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         order = Order.objects.get(order_number=tracking_number)
#         tracking = Tracking.objects.get(order=order)
#     except Order.DoesNotExist:
#         return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Tracking.DoesNotExist:
#         return Response({'error': 'Tracking information not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     serializer = TrackingSerializer(tracking)
#     return Response(serializer.data, status=status.HTTP_200_OK)     

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # Just for router basename resolution
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def create(self, request, *args, **kwargs):
        print("POST DATA:", request.data)
        print("POST DATA:", request.data['products'][0])
        try:
            client= Client.objects.get(user=request.user.id)
            order = self.queryset.create(client=client)
            order.products.set(request.data['products'])
            return Response({'message':'order created'}, status=status.HTTP_201_CREATED)
        except NameError:
            return Response({'message':NameError}, status=status.HTTP_400_BAD_REQUEST)
            

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(client__user=user).order_by('-date')
    
    @action(detail=False, methods=['get'], url_path='by-seller')
    def get_order_for_seller(self, request):
        seller = Seller.objects.get(user=request.user)
        if not seller:
            return Response({'error': 'seller_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(products__seller__id=seller.id).distinct()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['patch'], url_path='update-by-seller')
    def patch_order_for_seller(self, request):
        print(request.user)
        try:
            seller = Seller.objects.get(user=request.user)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

        order_id = request.query_params.get("id")  # <-- read from query string
        if not order_id:
            return Response({"error": "Order ID (id) is required in query params."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.filter(products__seller=seller).distinct().get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found or not related to this seller."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(order, data=request.data, partial=True)
        Tracking.objects.create(order=order, status='On route')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    

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


