from rest_framework import serializers
from .models import User, CustomerProfile, VendorProfile, UserAddress, ProductCategory, ProductList
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError


#  Craete user serializer
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=8, required=True, help_text='Password must be at least 8 characters and contain an uppercase letter, a lowercase letter, a number, and a special character.')
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, min_length=8, required=True, help_text="Please confirm your password.")
    username = serializers.CharField(read_only=True)

    USER_ROLE_CHOICES = [
        (User.Role.VENDOR, 'Vendor'),
        (User.Role.CUSTOMER, 'Customer')
    ]
    role = serializers.ChoiceField(choices=USER_ROLE_CHOICES, required=True, help_text="Choose your role: Vendor or Customer.")

    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'username', 'password', 'password2']
        read_only_fields = ['id']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        
        # Prevent role changes on update operations
        if self.instance and attrs.get('role') and attrs['role'] != self.instance.role:
            raise serializers.ValidationError({'role': 'The user role cannot be changed after creation.'})

        try:
            password_validation.validate_password(attrs['password'], user=self.instance)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

#  Change password serializer
class ChangeUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True, min_length=8, help_text='New password must be at least 8 characters and contain an uppercase letter, a lowercase letter, a number, and a special character.')
    new_password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True, min_length=8, help_text="Please confirm your new password.")

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        if not self.instance.check_password(old_password):
            raise serializers.ValidationError({'old_password': 'Old password is incorrect.'})
        elif attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password2': 'New passwords do not match.'})
        elif old_password == attrs['new_password']:
            raise serializers.ValidationError({'new_password': 'New password cannot be the same as the old password.'})
        try:
            password_validation.validate_password(new_password, user=self.instance)
        except DjangoValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return attrs
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

#  User profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']
        read_only_fields = ['id','username', 'role']

#  Customer profile serializer
class CustomerProfileSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ['user']

#  Vendor profile serializer
class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = '__all__'
        read_only_fields = ['user']

# User address
class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'

#  Category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory 
        fields = '__all__'
        read_only_fields = ['slug']

#  Product serializer
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductList
        fields = '__all__'
        read_only_fields = ['slug', 'product_price_after_discount', 'product_created_at', 'product_updated_at']

    def validate_product_name(self, value):
        if len(value)<3:
            raise serializers.ValidationError("Product name must be at least 3 characters long.")
        if not value[0].isalpha():
            raise serializers.ValidationError("Product name must start with an alphabet.")
        if not value[0].isupper():
            raise serializers.ValidationError("Product name must start with a capital letter.")
        return value
    def validate_product_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Product price must be greater than zero.")
        return value
    def validate_product_discount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Product discount must be greater than zero.")
        elif value >= 100:
            raise serializers.ValidationError("Product discount must be less than 100.")
        return value