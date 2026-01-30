from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models import (
    User, 
    CustomerProfile, 
    VendorProfile, 
    UserAddress, 
    ProductCategory
    )
from .serializers import ( 
    CreateUserSerializer,
    ChangeUserPasswordSerializer, 
    UserProfileSerializer,
    CustomerProfileSerializer, 
    VendorProfileSerializer,
    CategorySerializer,
    UserAddressSerializer
)
from .permissions import (
    IsAdminReadOnlyOrOwnerEdit,
    IsVendorOrAdminAllOrReadOnly, 
    IsVendorAndOwnerOrReadOnly,
    IsCustomerAndOwnerOrReadOnly,
    IsCustomerOrVendorAuthenticated 
)


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

class UserListView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

class UserAccountDeleteView(DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminReadOnlyOrOwnerEdit]

    def get_object(self):
        return self.request.user

class ChangeUserPasswordView(UpdateAPIView):
    serializer_class = ChangeUserPasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        serializer.save()       

class CustomerProfileView(ModelViewSet):
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsCustomerAndOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CustomerProfile.objects.none()
        if self.action == 'list':
            return CustomerProfile.objects.filter(user=self.request.user)
        return CustomerProfile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class VendorProfileView(ModelViewSet):
    serializer_class = VendorProfileSerializer
    permission_classes = [IsVendorAndOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return VendorProfile.objects.none()
        if self.action == 'list':
            return VendorProfile.objects.filter(user=self.request.user)
        return VendorProfile.objects.all()
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsVendorOrAdminAllOrReadOnly]
    lookup_field = 'slug'

class UserAddressView(ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsCustomerOrVendorAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserAddress.objects.none()
        return UserAddress.objects.filter(user=self.request.user)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

