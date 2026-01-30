from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import (
    UserCreateView,
    UserListView, 
    UserAccountDeleteView, 
    ChangeUserPasswordView, 
    UserProfileView, 
    CustomerProfileView, 
    VendorProfileView,
    UserAddressView,
    CategoryViewSet
)


# router
router = DefaultRouter()
# personal-info
router.register(r'customer-profile', CustomerProfileView, basename='customer_profile')
router.register(r'vendor-profile', VendorProfileView, basename='vendor_profile')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'user-address', UserAddressView, basename='user_address')
router.register(r'admin/user-list', UserListView, basename='user_list')

urlpatterns = [
    #  router urls
    path('', include(router.urls)),

    # signup
    path('signup/', UserCreateView.as_view(), name='signup'),

    # profile
    path('profile/', UserProfileView.as_view(), name='user_profile'),

    # login
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # change password
    path('change-password/', ChangeUserPasswordView.as_view(), name='change_password'),

    # deactivate
    path('deactivate/', UserAccountDeleteView.as_view(), name='user_account_delete'),

]
