from rest_framework import mixins, viewsets

from myslack import models

from ..serializers.reactions import CommentReactionSerializer, ReactionSerializer, ThreadReactionSerializer


class ReactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Reaction.objects.all()
    serializer_class = ReactionSerializer


class CommentReactionViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = models.CommentReaction.objects.all()
    serializer_class = CommentReactionSerializer


class ThreadReactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ThreadReaction.objects.all()
    serializer_class = ThreadReactionSerializer
