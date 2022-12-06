from rest_framework import serializers

from myslack import models


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Channel
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'members_count',
        )


class ChannelMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChannelMembership
        fields = (
            'id',
            'profile',
            'is_admin',
            'is_read_only',
        )
