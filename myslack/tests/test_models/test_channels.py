from django.test import TestCase

from myslack import factories, models


class ChannelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.workspace_1 = factories.WorkspaceFactory()
        cls.workspace_2 = factories.WorkspaceFactory()
        cls.channel = factories.ChannelFactory(workspace=cls.workspace_1)
        factories.ChannelMembershipFactory.create_batch(3, profile__workspace=cls.workspace_1, channel=cls.channel)
        factories.ChannelMembershipFactory.create_batch(3, profile__workspace=cls.workspace_2)

    def test_channel_model_members_count(self):
        self.assertEqual(self.channel.members_count, 3)

    def test_channel_queryset_members_count(self):
        channel = models.Channel.objects.with_members_count().get(id=self.channel.id)
        self.assertEqual(channel.members_count, 3)


