from django.db import models


class Thread(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    channel = models.ForeignKey(
        to='Channel',
        related_name='threads',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        to='Profile',
        related_name='threads',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Thread {self.id} at {self.channel}'


class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thread = models.ForeignKey(
        to='Thread',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        to='Profile',
        related_name='comments',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment {self.id} in {self.thread}'
