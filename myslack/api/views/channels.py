from rest_framework import mixins, viewsets

from myslack import models

from ..serializers.channels import ChannelMembershipSerializer, ChannelSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = models.Channel.objects.all().with_members_count()
    serializer_class = ChannelSerializer

    # TODO: create, update, delete - workspace admin only
    #  join channel
    #  add to channel
    #  search
    #  filter


class ChannelMembershipViewSet(viewsets.ModelViewSet):
    queryset = models.ChannelMembership.objects.all()
    serializer_class = ChannelMembershipSerializer
