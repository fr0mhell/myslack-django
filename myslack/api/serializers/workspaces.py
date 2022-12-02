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
        )


class InviteByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get('email')

        if models.Profile.objects.filter(user__email=email, workspace_id=self.context.get('workspace_id')).exists():
            raise ValidationError(f'Profile for email "{email}" already exists')
        return attrs
