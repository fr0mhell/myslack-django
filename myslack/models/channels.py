from django.db import models
from django.utils.text import slugify


class ChannelQuerySet(models.QuerySet):

    def with_members_count(self):
        return self.annotate(num_members=models.Count('channel_members'))


class Channel(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    workspace = models.ForeignKey(
        to='Workspace',
        related_name='workspaces',
        on_delete=models.CASCADE,
    )

    objects = ChannelQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('slug', 'workspace'),
                name='unique_channel_slug_per_workspace',
            ),
        ]
        ordering = ['slug']

    def __str__(self):
        return f'Channel "{self.slug}" at {self.workspace}'

    @property
    def members_count(self):
        return self.num_members if hasattr(self, 'num_members') else self.channel_members.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
        return f'{self.profile} in {self.channel}'
