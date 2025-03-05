from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return 'ADMIN' in request.user.roles
    
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return 'CUSTOMER' in request.user.roles
    
class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return 'VENDOR' in request.user.roles
    