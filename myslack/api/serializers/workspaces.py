from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from myslack import models


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workspace
        fields = (
            'id',
            'name',
            'description',
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = (
            'id',
            'full_name',
            'display_name',
            'email',
            'phone',
            'workspace',
        )
        read_only_fields = (
            'workspace',
        )


class InviteByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get('email')

        if models.Profile.objects.filter(user__email=email, workspace_id=self.context.get('workspace_id')).exists():
            raise ValidationError(f'Profile for email "{email}" already exists')
        return attrs


class SearchSerializer(serializers.Serializer):
    search_string = serializers.CharField(min_length=3, required=False)
    channels = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)
    author = serializers.IntegerField(min_value=1, required=False)
    created_from = serializers.DateField(required=False)
    created_to = serializers.DateField(required=False)

    def __init__(self, user_channel_ids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._user_channel_ids = user_channel_ids

    def validate(self, attrs):
        if not attrs:
            raise ValidationError('You have to pass at least one search parameter')

        if (created_from := attrs.get('created_from')) and (created_to := attrs.get('created_to')):
            if created_from > created_to:
                raise ValidationError(
                    'Wrong date range. "created_to" must be equal or greater than "created_from"'
                )
        return attrs

    def to_representation(self, data):
        internal = super().to_representation(data)
        result = {'text__icontains': internal['search_string']}

        # Search among channels visible for user
        if channels := internal.get('channels'):
            result.update({'channel_id__in': set(channels) & set(self._user_channel_ids)})
        else:
            result.update({'channel_id__in': self._user_channel_ids})

        if author := internal.get('author'):
            result.update({'author': author})

        if created_from := internal.get('created_from'):
            result.update({'created_at__gte': created_from})

        if created_to := internal.get('created_to'):
            result.update({'created_at__lte': created_to})

        return result
