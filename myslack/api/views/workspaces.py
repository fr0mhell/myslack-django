import logging

from django.contrib.auth import get_user_model
from rest_framework import mixins, response, status, viewsets
from rest_framework.decorators import action

from myslack import models

from ..permissions import IsWorkspaceAdminPermission
from ..serializers.workspaces import InviteByEmailSerializer, ProfileSerializer, WorkspaceSerializer

logger = logging.getLogger(__name__)

User = get_user_model()


class WorkspaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(profiles__user=self.request.user)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if workspace_id := self.kwargs.get('pk'):
            context.update({'workspace_id': workspace_id})
        return context

    @action(
        detail=True,
        methods=['post'],
        url_path='invite',
        serializer_class=InviteByEmailSerializer,
        permission_classes=(IsWorkspaceAdminPermission, ),
    )
    def invite_by_email(self, request, pk=None):
        """Invite new user to Workspace by email.

        Dummy implementation, only log entry created.

        """
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        logger.info(f'Invitation to {serializer.validated_data["email"]} successfully sent')
        return response.Response(status=status.HTTP_201_CREATED)


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Profile.objects.all()
    serializer_class = ProfileSerializer

    # TODO: Admin can edit all profiles in workspace
    # TODO: User can edit his profile via "my profile" action
