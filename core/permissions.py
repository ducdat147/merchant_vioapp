from rest_framework import permissions

class HasMerchantPermission(permissions.BasePermission):
    message = "You need to create a merchant before performing this action"

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and hasattr(request.user, 'merchant')) 