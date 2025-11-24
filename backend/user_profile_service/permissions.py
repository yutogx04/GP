from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read-only for any request, write only for admin users."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
