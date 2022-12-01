from rest_framework import mixins, viewsets
from ..serializers.workspaces import WorkspaceSerializer, ProfileSerializer
from myslack import models


class WorkspaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    # TODO: add dummy "invite with email" action, available to admin only


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
