
from rest_framework import permissions
from .models import User

# Admin and Vendor can edit and add categories Customers only view categories
class IsVendorOrAdminAllOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and (request.user.role == User.Role.ADMINISTRATOR)

# Customer only access
class IsCustomerAndOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  return request.user and request.user.is_authenticated
        if request.method == 'POST':    return request.user and request.user.is_authenticated and request.user.role == User.Role.CUSTOMER
        return request.user and request.user.is_authenticated
    def has_object_permission(self, request,view, obj):
        if request.method in permissions.SAFE_METHODS:  return request.user and request.user.is_authenticated
        return obj.user == request.user

# Vendor only access
class IsVendorAndOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  return request.user and request.user.is_authenticated
        if request.method == 'POST':    return request.user and request.user.is_authenticated and request.user.role == User.Role.VENDOR
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

