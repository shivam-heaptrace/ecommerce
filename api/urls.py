from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/create-admin', AdminUserCreateAPIView.as_view(), name='create-admin'),
    path('customer/signup', CustomerSignUpAPIView.as_view(), name='customer-signup'),
    path('user/login', UserLoginAPIView.as_view(), name='user-login'),
]