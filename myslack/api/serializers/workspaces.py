from rest_framework import serializers
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

