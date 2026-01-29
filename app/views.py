
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User, CustomerProfile, VendorProfile, ProductCategory
from .serializers import ( 
    UserProfileSerializer, 
    ChangeUserPasswordSerializer, 
    CustomerProfileSerializer, 
    VendorProfileSerializer,
    CategorySerializer,
    UserAddressSerializer
)
from .permissions import IsVendorOrAdminAllOrReadOnly, IsCustomerAndOwnerOrReadOnly, IsVendorAndOwnerOrReadOnly

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

class UserAccountDeleteView(DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserProfileView(RetrieveAPIView):
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
    # authentication_classes = 

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

class UserAddressView(ModelViewSet):
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return UserAddress.objects.none()
        return UserAddress.objects.filter(user=self.request.user)



