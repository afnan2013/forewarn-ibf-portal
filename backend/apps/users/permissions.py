from rest_framework import permissions


class HasUserViewPermission(permissions.BasePermission):
    """
    Custom permission for viewing users
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('users.view_user')


class HasUserChangePermission(permissions.BasePermission):
    """
    Custom permission for changing users
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('users.change_user')


class HasUserDeletePermission(permissions.BasePermission):
    """
    Custom permission for deleting users
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.has_perm('users.delete_user')


class CannotModifySuperuser(permissions.BasePermission):
    """
    Permission to prevent modification of superuser accounts
    """
    def has_object_permission(self, request, view, obj):
        # Allow read operations for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Prevent modification of superuser accounts
        return not obj.is_superuser


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it,
    or users with admin permissions.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions only to the owner or admin users
        return (
            obj == request.user or 
            request.user.has_perm('users.change_user')
        )
