from django.urls import reverse
from django.utils.text import slugify
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from myslack import factories, models

fake = Faker()
Faker.seed(0)


class ChannelsAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = cls.client_class()
        cls.admin_client = cls.client_class()
        cls.workspace = factories.WorkspaceFactory()
        cls.channel = factories.ChannelFactory(workspace=cls.workspace)
        cls.profile_1 = factories.ProfileFactory(workspace=cls.workspace, is_workspace_admin=True)
        cls.profile_2 = factories.ProfileFactory(workspace=cls.workspace)
        cls.profile_3 = factories.ProfileFactory()

    def setUp(self) -> None:
        self.admin_client.force_authenticate(self.profile_1.user)
        self.client.force_authenticate(self.profile_2.user)

    def test_create_channel(self):
        """Check only Workspace Admin can create a Channel."""
        url = reverse('myslack:channels-list', args=[self.workspace.id])
        data = {'name': 'New channel', 'description': 'Channel description'}

        self.assertEqual(models.Channel.objects.count(), 1)

        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.Channel.objects.count(), 1)

        response = self.admin_client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Channel.objects.count(), 2)

    def test_update_channel(self):
        """Check only Workspace Admin can edit a Channel."""
        url = reverse('myslack:channels-detail', args=[self.workspace.id, self.channel.id])
        data = {'name': 'Updated channel', 'description': 'Updated channel description'}

        response = self.client.put(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.admin_client.put(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.channel.refresh_from_db()
        self.assertEqual(self.channel.name, data['name'])
        self.assertEqual(self.channel.slug, slugify(data['name']))
        self.assertEqual(self.channel.description, data['description'])

    def test_delete_channel(self):
        """Check only Workspace Admin can delete a Channel."""
        url = reverse('myslack:channels-detail', args=[self.workspace.id, self.channel.id])

        self.assertEqual(models.Channel.objects.count(), 1)

        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.Channel.objects.count(), 1)

        response = self.admin_client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.Channel.objects.count(), 0)

    def test_join_channel(self):
        """Check only workspace member can join a channel."""
        url = reverse('myslack:channels-join', args=[self.workspace.id, self.channel.id])
        self.assertEqual(models.ChannelMembership.objects.count(), 0)

        response = self.client.post(path=url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.ChannelMembership.objects.count(), 1)

        # Cannot join multiple times
        response = self.client.post(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.ChannelMembership.objects.count(), 1)

        self.client.force_authenticate(self.profile_3.user)
        response = self.client.post(path=url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(models.ChannelMembership.objects.count(), 1)

    def test_add_to_channel(self):
        """Check only channel member can add another workspace member to channel."""
        url = reverse('myslack:channels-add', args=[self.workspace.id, self.channel.id])
        data = {'profile': self.profile_1.id}

        # Not channel member cannot add another profile to channel
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        factories.ChannelMembershipFactory(channel=self.channel, profile=self.profile_2)
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.ChannelMembership.objects.count(), 2)

        # Cannot add same profile multiple times
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.ChannelMembership.objects.count(), 2)

        # Cannot add member of another workspace to channel
        data = {'profile': self.profile_3.id}
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(models.ChannelMembership.objects.count(), 2)

    def test_kick_from_channel(self):
        url = reverse('myslack:channels-kick', args=[self.workspace.id, self.channel.id])
        data = {'profile': self.profile_1.id}
        factories.ChannelMembershipFactory(channel=self.channel, profile=self.profile_2)

        # Not channel member cannot kick from channel
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Not Workspace admin cannot kick from channel
        factories.ChannelMembershipFactory(channel=self.channel, profile=self.profile_1)
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.profile_2.is_workspace_admin = True
        self.profile_2.save()
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(models.ChannelMembership.objects.count(), 1)

        # 404 returned when trying to kick not a channel member
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
