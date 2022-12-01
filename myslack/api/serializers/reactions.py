from rest_framework import serializers
from myslack import models


class ReactionSerializer(serializers.ModelSerializer):
    # TODO: Replace with example of custom list serialization
    class Meta:
        model = models.Reaction
        fields = (
            'slug',
        )


class ThreadReactionSerializer(serializers.ModelSerializer):
    # TODO: Add "is_my" field
    class Meta:
        model = models.ThreadReaction
        fields = (
            'id',
            'profile',
            'thread',
            'reaction',
        )


class CommentReactionSerializer(serializers.ModelSerializer):
    # TODO: Add "is_my" field
    class Meta:
        model = models.CommentReaction
        fields = (
            'id',
            'profile',
            'comment',
            'reaction',
        )
