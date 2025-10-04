from rest_framework import permissions
from .models import User


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Role.ADMIN)
