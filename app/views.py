
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import User, CustomerProfile, VendorProfile
from .serializers import CreateUserSerializers, UserProfileSerializer, ChangeUserPasswordSerializer, CustomerProfileSerializer, VendorProfileSerializer



class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializers
    permission_classes = [AllowAny]


class UserAccountDeleteView(DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ChangeUserPasswordView(UpdateAPIView):
    serializer_class = ChangeUserPasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def get_object(self):
        return self.request.user
 

class UserIdView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class CustomerProfileView(ModelViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomerProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VendorProfileView(ModelViewSet):
    serializer_class = VendorProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VendorProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

