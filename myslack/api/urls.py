from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.channels import ChannelViewSet
from .views.reactions import CommentReactionViewSet, ReactionViewSet, ThreadReactionViewSet
from .views.threads import CommentViewSet, ThreadViewSet
from .views.workspaces import ProfileViewSet, WorkspaceViewSet

# Create a router and register our viewsets with it.
v1_router = DefaultRouter()
# Top-level API
v1_router.register('workspaces', WorkspaceViewSet, basename='workspaces')
v1_router.register('reactions', ReactionViewSet, basename='reactions')
# Workspace-related API
v1_router.register(
    r'workspaces/(?P<workspace_id>\d+)/profiles',
    ProfileViewSet,
    basename='profiles',
)
v1_router.register(
    r'workspaces/(?P<workspace_id>\d+)/channels',
    ChannelViewSet,
    basename='channels',
)
# Channel-related API
v1_router.register(
    r'workspaces/(?P<workspace_id>\d+)/channels/(?P<channel_id>\d+)/threads',
    ThreadViewSet,
    basename='threads',
)
# Thread-related API
v1_router.register(
    r'workspaces/(?P<workspace_id>\d+)/channels/(?P<channel_id>\d+)/threads/(?P<thread_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
# TODO: probably don't need as separate viewsets
v1_router.register(
    'thread-reactions',
    ThreadReactionViewSet,
    basename='thread-reactions',
)
v1_router.register(
    'comment-reactions',
    CommentReactionViewSet,
    basename='comment-reactions',
)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('v1', include(v1_router.urls)),
]
