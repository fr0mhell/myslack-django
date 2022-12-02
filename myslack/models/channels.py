from django.db import models


class Channel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    workspace = models.ForeignKey(
        to='Workspace',
        related_name='workspaces',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('slug', 'workspace'),
                name='unique_channel_slug_per_workspace',
            ),
        ]
        ordering = ['slug']

    def __str__(self):
        return f'Channel "{self.slug}" at '


class ChannelMembership(models.Model):
    channel = models.ForeignKey(
        to='Channel',
        related_name='channel_members',
        on_delete=models.PROTECT,
    )
    profile = models.ForeignKey(
        to='Profile',
        related_name='channel_memberships',
        on_delete=models.CASCADE,
    )
    is_admin = models.BooleanField(default=False)
    is_read_only = models.BooleanField(default=False)

    class Meta:
        ordering = ['profile', 'channel']

    def __str__(self):
        return f'Comment {self.id} in {self.thread}'
