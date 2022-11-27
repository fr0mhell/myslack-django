from django.db import models


class Reaction(models.Model):
    slug = models.SlugField(primary_key=True)

    def __str__(self):
        return self.slug


class ThreadReaction(models.Model):
    profile = models.ForeignKey(
        to='Profile',
        related_name='thread_reactions',
        on_delete=models.CASCADE,
    )
    thread = models.ForeignKey(
        to='Thread',
        related_name='thread_reactions',
        on_delete=models.CASCADE,
    )
    reaction = models.ForeignKey(
        to='Reaction',
        related_name='thread_reactions',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.reaction} to {self.thread} by {self.profile}'


class CommentReaction(models.Model):
    profile = models.ForeignKey(
        to='Profile',
        related_name='comment_reactions',
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        to='Comment',
        related_name='comment_reactions',
        on_delete=models.CASCADE,
    )
    reaction = models.ForeignKey(
        to='Reaction',
        related_name='comment_reactions',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.reaction} to {self.comment} by {self.profile}'
