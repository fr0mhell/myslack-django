from rest_framework import mixins, viewsets
from ..serializers.channels import ChannelSerializer, ChannelMembershipSerializer
from myslack import models


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = models.Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelMembershipViewSet(viewsets.ModelViewSet):
    queryset = models.ChannelMembership.objects.all()
    serializer_class = ChannelMembershipSerializer
