from rest_framework import viewsets

from myslack import models

from ..serializers.threads import CommentSerializer, ThreadSerializer


class ThreadViewSet(viewsets.ModelViewSet):
    queryset = models.Thread.objects.all()
    serializer_class = ThreadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = CommentSerializer
