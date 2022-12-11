from rest_framework import response, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from myslack import models

from ..permissions import IsChannelMember, IsWorkspaceAdminOrReadOnly, IsWorkspaceMember
from ..serializers.channels import ChannelMembershipSerializer, ChannelSerializer
from .mixins import WorkspaceRelatedMixin


class ChannelViewSet(WorkspaceRelatedMixin, viewsets.ModelViewSet):
    queryset = models.Channel.objects.all().with_members_count()
    serializer_class = ChannelSerializer
    permission_classes = (IsWorkspaceAdminOrReadOnly, )
    search_fields = ['name', 'description']

    @property
    def channel_id(self):
        return self.kwargs.get('pk')

    def perform_create(self, serializer):
        serializer.save(workspace_id=self.workspace_id)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsWorkspaceMember, ),
    )
    def join(self, request, *args, **kwargs):
        profile = get_object_or_404(models.Profile, workspace_id=self.workspace_id, user=self.request.user)
        _, created = models.ChannelMembership.objects.get_or_create(profile=profile, channel_id=self.kwargs['pk'])
        if created:
            return response.Response(status=status.HTTP_201_CREATED)
        return response.Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        serializer_class=ChannelMembershipSerializer,
        permission_classes=(IsChannelMember, ),
    )
    def add(self, request, *args, **kwargs):
        """Add another Profile to a Channel."""
        profile = self._serialize_profile(request)
        member, created = models.ChannelMembership.objects.get_or_create(channel_id=self.channel_id, profile=profile)
        if created:
            return response.Response(status=status.HTTP_201_CREATED)
        return response.Response(status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=(IsWorkspaceAdminOrReadOnly, IsChannelMember),
        serializer_class=ChannelMembershipSerializer,
    )
    def kick(self, request, *args, **kwargs):
        """Kick a channel member."""
        profile = self._serialize_profile(request)
        member = get_object_or_404(models.ChannelMembership.objects.all(), channel_id=self.channel_id, profile=profile)
        member.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def _serialize_profile(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return get_object_or_404(
            queryset=models.Profile.objects.all(),
            workspace_id=self.workspace_id,
            id=serializer.data['profile'],
        )
