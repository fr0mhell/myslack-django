from django.shortcuts import get_object_or_404
from rest_framework import permissions

from ..models import ChannelMembership, Profile


def _get_profile(request, view):
    return Profile.objects.filter(user=request.user, workspace_id=view.workspace_id).first()


def _get_channel_member(request, view):
    profile = _get_profile(request, view)
    return ChannelMembership.objects.filter(profile=profile, channel_id=view.channel_id).first()


class IsWorkspaceAdminOrReadOnly(permissions.BasePermission):
    """Check if a User has admin Profile in the Workspace."""

    def has_permission(self, request, view):
        profile = _get_profile(request, view)
        return (profile and profile.is_workspace_admin) or request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = get_object_or_404(Profile, user=request.user, workspace_id=view.workspace_id)
        return obj.profile_id == profile.id or request.method in permissions.SAFE_METHODS


class IsWorkspaceMember(permissions.BasePermission):
    def has_permission(self, request, view):
        profile = _get_profile(request, view)
        return profile is not None or request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsChannelMember(permissions.BasePermission):
    def has_permission(self, request, view):
        member = _get_channel_member(request, view)
        return member is not None or request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

