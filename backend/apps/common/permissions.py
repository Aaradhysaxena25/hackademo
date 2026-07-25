"""
Custom permissions for CodePilot API.
"""

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsRepositoryOwner(BasePermission):
    """
    Custom permission to only allow repository owners to access resources.
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "repository"):
            return obj.repository.owner == request.user
        return obj.owner == request.user


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to non-admin users.
    """

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return request.user and request.user.is_staff
