from rest_framework import serializers
from .models import User, CustomerProfile, VendorProfile
from .validators import validate_password_strength

#  Craete user serializer
class CreateUserSerializers(serializers.ModelSerializer):
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
        fields = ['email', 'role', 'username', 'password', 'password2']

    def validate_password(self, value):
        validate_password_strength(value)
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        
        # Prevent role changes on update operations
        if self.instance and attrs.get('role') and attrs['role'] != self.instance.role:
            raise serializers.ValidationError({'role': 'The user role cannot be changed after creation.'})

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

    def validate_new_password(self, value):
        validate_password_strength(value)
        return value

    def validate(self, attrs):

        old_password = attrs.get('old_password')

        if not self.instance.check_password(old_password):
            raise serializers.ValidationError({'old_password': 'Old password is incorrect.'})

        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password2': 'New passwords do not match.'})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


# User profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']


class CustomerProfileSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['user', 'profile_pic', 'phone_number', 'date_of_birth', 'gender', 'age']

class VendorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorProfile
        fields = ['user', 'logo', 'phone_number', 'company_name', 'business_registration_number', 'gst_id', 'website']


