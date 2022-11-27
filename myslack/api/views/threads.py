from rest_framework import viewsets
from ..serializers.threads import ThreadSerializer, CommentSerializer
from myslack import models


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = models.Thread.objects.all()
    serializer_class = ThreadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer
