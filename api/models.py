from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=Role.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} by {self.customer.email}'
