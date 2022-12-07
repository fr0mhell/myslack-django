import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from factory import fuzzy

from . import models

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.LazyFunction(lambda: make_password('pi3.1415'))

    @factory.lazy_attribute
    def username(self):
        slug_name = slugify(f'{self.first_name} {self.last_name}')
        return f'{slug_name}@example.com'

    @factory.lazy_attribute
    def email(self):
        slug_name = slugify(self.username)
        return f'{slug_name}@example.com'


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
