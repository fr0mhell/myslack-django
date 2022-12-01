from rest_framework import mixins, viewsets
from ..serializers.reactions import ReactionSerializer, CommentReactionSerializer, ThreadReactionSerializer
from myslack import models


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
