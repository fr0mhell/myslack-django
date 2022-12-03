from rest_framework import mixins, viewsets

from myslack import models

from ..serializers.channels import ChannelMembershipSerializer, ChannelSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = models.Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelMembershipViewSet(viewsets.ModelViewSet):
    queryset = models.ChannelMembership.objects.all()
    serializer_class = ChannelMembershipSerializer
