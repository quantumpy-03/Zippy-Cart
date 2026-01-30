
from rest_framework import permissions
from .models import User

class IsAdminReadOnlyOrOwnerEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if  request.user and request.user.is_authenticated and request.user.is_superuser:
            return request.method in permissions.SAFE_METHODS
        if request.user and request.user.is_authenticated and (request.user.role == User.Role.VENDOR or request.user.role == User.Role.CUSTOMER):
            return obj.pk == request.user.pk
        return False


# Admin and Vendor can edit and add categories Customers only view categories
class IsVendorOrAdminAllOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (request.user.role == User.Role.ADMINISTRATOR)

# Customer only have full access
class IsCustomerAndOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  return request.user and request.user.is_authenticated
        if request.method == 'POST':    return request.user and request.user.is_authenticated and request.user.role == User.Role.CUSTOMER
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request,view, obj):
        if request.method in permissions.SAFE_METHODS:  return request.user and request.user.is_authenticated
        return obj.user == request.user

# Vendor only have full access
class IsVendorAndOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  return request.user and request.user.is_authenticated
        if request.method in ('POST', 'PUT', 'PATCH', 'DELETE'):    return request.user and request.user.is_authenticated and request.user.role == User.Role.VENDOR
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  return request.user and request.user.is_authenticated
        return obj.user == request.user

# Address update
class IsCustomerOrVendorAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (request.user.role == User.Role.CUSTOMER or request.user.role == User.Role.VENDOR)
                
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return obj.user == request.user

