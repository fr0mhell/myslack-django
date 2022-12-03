from django.shortcuts import get_object_or_404
from rest_framework import permissions

from ..models import Profile


class IsWorkspaceAdminOrReadOnly(permissions.BasePermission):
    """Check if a User has admin Profile in the Workspace."""

    def has_permission(self, request, view):
        return self._is_workspace_admin(request, view) or request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self._is_workspace_admin(request, view) or request.method in permissions.SAFE_METHODS

    def _is_workspace_admin(self, request, view):
        profile = get_object_or_404(Profile, user=request.user, workspace_id=view.workspace_id)
        return profile.is_workspace_admin


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = get_object_or_404(Profile, user=request.user, workspace_id=view.workspace_id)
        return obj.profile_id == profile.id or request.method in permissions.SAFE_METHODS
