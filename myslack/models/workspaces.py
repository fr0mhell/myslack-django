from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Workspace(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'Workspace "{self.name}"'


class Profile(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='profiles',
        on_delete=models.CASCADE,
    )
    workspace = models.ForeignKey(
        to=Workspace,
        related_name='profiles',
        on_delete=models.CASCADE,
    )
    is_workspace_admin = models.BooleanField(default=False)

    full_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} ({self.user}) at {self.workspace}'
