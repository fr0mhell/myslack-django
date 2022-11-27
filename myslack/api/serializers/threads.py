from rest_framework import serializers
from myslack import models


class ThreadSerializer(serializers.ModelSerializer):
    # TODO: Add "is_my" field
    class Meta:
        model = models.Thread
        fields = (
            'id',
            'text',
            'created_at',
            'updated_at',
            'channel',
        )


class CommentSerializer(serializers.ModelSerializer):
    # TODO: Add "is_my" field
    class Meta:
        model = models.Comment
        fields = (
            'id',
            'text',
            'created_at',
            'updated_at',
            'thread',
        )


# TODO: Make example of custom serializer for Search Results
