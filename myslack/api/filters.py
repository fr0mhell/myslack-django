import django_filters

from .. import models


class ProfileFilter(django_filters.rest_framework.FilterSet):
    channel = django_filters.CharFilter(method='channel_filter')

    class Meta:
        model = models.Profile
        fields = (
            'channel',
        )

    def channel_filter(self, queryset, name, value):
        return queryset.filter(channel_memberships__channel_id=value)
