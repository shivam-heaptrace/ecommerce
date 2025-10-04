from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Repsponse
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Product, Order
from .serializers import UserRegistrationSerializer, UserSerializer, ProductSerializer, OrderSerializer
from .permissions import IsAdminUser


class AdminUserCreateAPIView(generics.CreateAPIView):
    """
    API for creating an admin user
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegistrarionSerializer
    
    def perform_create(self, serializer):
        serializer.save(role=User.Role.ADMIN)


class CustomerSignUpAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def perform_create(self, serializer):
        serializer.save(role=User.Role.CUSTOMER)
        
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({"Message": "Sign Up Successful"}, status=status.HTTP_201_CREATED) [cite: 76]
    
    
    class UserLoginAPIView(ObtainAuthToken):
        def post(self, request, *args, **kwargs):
            serializer = self.serializer_class(data=request.data, context={'reqeust':request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'id': user.pk,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
            })


class ProductViewSet(viewsets.ModelViewSet):
    """
    API for produtcs
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
def get_permissions(self):
    """
    Instantiates and returns the list of permissions
    """
    if self.action in ['create', 'update', 'partial_update', 'destroy']:
        self.permission_classes = [IsAdminUser]    
    else:
        self.permission_classes = [IsAuthenticated]
    return super(ProductViewSet, self).get_permissons()


class UserViewSet(viewsets.ModelViewSet):
    """
    API to get all users, search users, update user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'email', 'first_name']
    

class OrderViewSet(viewsets.ModelViewSet):
    """
    API to order products and view a customer's products
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This view should return a list if all the orders
        """
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return Order.objects.all()
        return Order.objects.filter(customer=user)
    
    def perform_create(self, )