from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.workspaces import WorkspaceViewSet, ProfileViewSet
from .views.threads import ThreadViewSet, CommentViewSet
from .views.reactions import ReactionViewSet, CommentReactionViewSet, ThreadReactionViewSet
from .views.channels import ChannelMembershipViewSet, ChannelViewSet

# Create a router and register our viewsets with it.
v1_router = DefaultRouter()
v1_router.register('workspaces', WorkspaceViewSet, basename='workspaces')
v1_router.register('profiles', ProfileViewSet, basename='profiles')
v1_router.register('threads', ThreadViewSet, basename='threads')
v1_router.register('comments', CommentViewSet, basename='comments')
v1_router.register('channels', ChannelViewSet, basename='channels')
v1_router.register('channel-membership', ChannelMembershipViewSet, basename='channel-membership')
v1_router.register('reactions', ReactionViewSet, basename='reactions')
v1_router.register('comment-reactions', CommentReactionViewSet, basename='comment-reactions')
v1_router.register('thread-reactions', ThreadReactionViewSet, basename='thread-reactions')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
