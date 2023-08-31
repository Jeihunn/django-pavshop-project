from rest_framework import permissions


class IsOwnerOrSuperuserCanDeleteOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Anyone can just do a GET operation
        if request.method in permissions.SAFE_METHODS:
            return True

        # Comment owner can update or delete, superuser can delete
        if request.method == "DELETE":
            return obj.user == request.user or request.user.is_superuser

        return obj.user == request.user
