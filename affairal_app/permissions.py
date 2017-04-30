from rest_framework import permissions


class IsAdminOrNewUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return (obj.owner == request.user) or request.user.is_staff


class IsSelfOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return (obj.user.username == request.user.username) or request.user.is_staff