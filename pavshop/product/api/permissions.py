from rest_framework import permissions


class IsSuperuserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Anyone can perform safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is a superuser
        return request.user.is_superuser
