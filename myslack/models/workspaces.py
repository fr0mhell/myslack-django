from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Workspace(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField()

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

    full_name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.full_name} ({self.user}) at {self.workspace}'
