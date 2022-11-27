from django.contrib import admin
from . import models


@admin.register(models.Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ChannelMembership)
class ChannelMembershipAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Reaction)
class ReactionAdmin(admin.ModelAdmin):
    ...


@admin.register(models.ThreadReaction)
class ThreadReactionAdmin(admin.ModelAdmin):
    ...


@admin.register(models.CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    ...
