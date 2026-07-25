"""
Custom permissions for the repositories app.
"""

from rest_framework.permissions import BasePermission


class IsRepositoryOwner(BasePermission):
    """
    Only allow the owner of a repository to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id
