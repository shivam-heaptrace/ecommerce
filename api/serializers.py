from rest_framework import serializers
from .models import User, Product, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'role']

    def create(self, validated_data):
        # Create user with a hashed password
        return User.objects.create_user(            
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data.get('role', User.Role.CUSTOMER) # Default to Customer
        )        


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price']


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    customer_id = serializers.IntegerField(source='customer.id', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'products', 'product_ids', 'created_at']

        def create(self, validated_data):
            product_ids = validated_data.pop('product_ids')
            order = Order.objects.create(**validated_data)

            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                order.products.add(product)

            return order
