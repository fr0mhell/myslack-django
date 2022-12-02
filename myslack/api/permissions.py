from rest_framework import permissions

from ..models import Profile


class IsWorkspaceAdminPermission(permissions.BasePermission):
    """Check if a User has admin Profile in the Workspace."""
    def has_permission(self, request, view):
        workspace_pk = view.kwargs.get('pk')
        profile = Profile.objects.filter(user=request.user, workspace_id=workspace_pk).first()
        return profile.is_workspace_admin

    def has_object_permission(self, request, view, obj):
        workspace_pk = view.kwargs.get('pk')
        profile = Profile.objects.filter(user=request.user, workspace_id=workspace_pk).first()
        return profile.is_workspace_admin
