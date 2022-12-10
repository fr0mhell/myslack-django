import random

import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from factory import fuzzy
from faker import Faker

from . import models

fake = Faker()
Faker.seed(0)
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.LazyFunction(lambda: make_password('pi3.1415'))
    email = factory.Faker('email')

    @factory.lazy_attribute
    def username(self):
        return slugify(f'{fake.user_name()} {fake.slug()}')


class WorkspaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Workspace

    name = factory.Faker('company')
    description = fuzzy.FuzzyText(length=1024)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile

    user = factory.SubFactory(UserFactory)
    workspace = factory.SubFactory(WorkspaceFactory)

    full_name = factory.Faker('name')
    display_name = factory.Faker('name')
    email = factory.Faker('ascii_email')
    phone = factory.Faker('phone_number')


class ChannelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Channel

    name = factory.Faker('company')
    description = fuzzy.FuzzyText(length=1024)
    workspace = factory.SubFactory(WorkspaceFactory)


class ChannelMembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ChannelMembership

    profile = factory.SubFactory(ProfileFactory)
    channel = factory.SubFactory(ChannelFactory, workspace=factory.SelfAttribute('..profile.workspace'))


class ThreadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Thread

    author = factory.SubFactory(ProfileFactory)
    channel = factory.SubFactory(ChannelFactory, workspace=factory.SelfAttribute('..author.workspace'))
    text = fuzzy.FuzzyText(length=1024)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Comment

    thread = factory.SubFactory(ThreadFactory)
    author = factory.SubFactory(ProfileFactory, workspace=factory.SelfAttribute('..thread.channel.workspace'))
    text = fuzzy.FuzzyText(length=1024)


class ThreadReactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ThreadReaction

    thread = factory.SubFactory(ThreadFactory)
    profile = factory.SubFactory(ProfileFactory, workspace=factory.SelfAttribute('..thread.channel.workspace'))

    @factory.lazy_attribute
    def reaction(self):
        return random.choice(models.Reaction.objects.all())


class CommentReactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CommentReaction

    comment = factory.SubFactory(CommentFactory)
    profile = factory.SubFactory(ProfileFactory, workspace=factory.SelfAttribute('..comment.thread.channel.workspace'))

    @factory.lazy_attribute
    def reaction(self):
        return random.choice(models.Reaction.objects.all())
