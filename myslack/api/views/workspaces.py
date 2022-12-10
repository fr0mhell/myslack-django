import logging

from django.contrib.auth import get_user_model
from rest_framework import mixins, response, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS

from myslack import models

from ..permissions import IsOwnerOrReadOnly, IsWorkspaceAdminOrReadOnly
from ..serializers.workspaces import InviteByEmailSerializer, ProfileSerializer, WorkspaceSerializer
from .mixins import WorkspaceRelatedMixin
from ..filters import ProfileFilter

logger = logging.getLogger(__name__)

User = get_user_model()


class WorkspaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    pagination_class = None

    @property
    def workspace_id(self):
        return self.kwargs.get('pk')

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
        permission_classes=(IsWorkspaceAdminOrReadOnly,),  # TODO: Check authentication
    )
    def invite_by_email(self, request, pk=None, *args, **kwargs):
        """Invite new user to Workspace by email.

        Dummy implementation, only log entry created.

        """
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        logger.info(f'Invitation to {serializer.validated_data["email"]} successfully sent')
        return response.Response(status=status.HTTP_201_CREATED)


class ProfileViewSet(
    WorkspaceRelatedMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsWorkspaceAdminOrReadOnly, )
    filterset_class = ProfileFilter
    search_fields = [
        'full_name',
        'display_name',
        'email',
        'phone',
    ]

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='my-profile',
        url_name='my-profile',
        permission_classes=(IsOwnerOrReadOnly, ),
    )
    def my_profile(self, request, *args, **kwargs):
        """Allows to retrieve or edit User's own profile.

        Based on `retrieve` and `update` methods.

        """
        qs = self.filter_queryset(self.get_queryset())
        profile = get_object_or_404(qs, user_id=self.request.user.id)

        if request.method in SAFE_METHODS:
            serializer = self.get_serializer(profile)
        else:
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return response.Response(serializer.data)
