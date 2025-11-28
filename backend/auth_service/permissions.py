from rest_framework import permissions

def _check_role(user, role):
    return bool(user and user.is_authenticated and getattr(user, "role", None) == role)

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_role(request.user, "student")

class IsHospitalAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_role(request.user, "hospital_admin")

class IsFacultyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_role(request.user, "faculty_admin")

class IsEncadrant(permissions.BasePermission):
    def has_permission(self, request, view):
        return _check_role(request.user, "encadrant")

class IsProfileComplete(permissions.BasePermission):
    message = "Profile not complete."
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_profile_complete)
