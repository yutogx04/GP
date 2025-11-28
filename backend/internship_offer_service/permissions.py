from rest_framework import permissions

# Simple role-based checks using user.role (works with auth_service.User)
class IsHospitalAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "role", None) == "hospital_admin")

class IsAuthenticatedAndProfileComplete(permissions.BasePermission):
    message = "Complete your profile to perform this action."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_profile_complete", False) and getattr(request.user, "email_verified", False))
