from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsAdmin(permissions.BasePermission):
    """Allows access only to admin users. """
    message = "Only Admins are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'ADMIN' in request.user.roles)


class IsCustomer(permissions.BasePermission):
    """Allows access only to admin users. """
    message = "Only Admins are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'CUSTOMER' in request.user.roles)


class IsVendor(permissions.BasePermission):
    """Allows access only to talent users. """
    message = "Only Regular users are authorized to perform this action."

    def has_permission(self, request, view):
        return bool(request.user and request.user.roles and 'VENDOR' in request.user.roles)
