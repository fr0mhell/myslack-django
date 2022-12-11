from django.urls import reverse, reverse_lazy
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from myslack import factories, models

fake = Faker()
Faker.seed(0)


class SearchAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = cls.client_class()
        cls.workspace = factories.WorkspaceFactory()
        cls.url = reverse_lazy('myslack:workspaces-search', args=[cls.workspace.id])

        cls.channel_1 = factories.ChannelFactory(workspace=cls.workspace)
        cls.profile = factories.ProfileFactory(workspace=cls.workspace)
        factories.ChannelMembershipFactory(profile=cls.profile, channel=cls.channel_1)

        cls.thread_1 = factories.ThreadFactory(author=cls.profile, channel=cls.channel_1, text='Hello')
        cls.comment_1 = factories.CommentFactory(thread=cls.thread_1, text='Bye-bye')
        cls.comment_2 = factories.CommentFactory(thread=cls.thread_1, text='heLlo')

        cls.thread_2 = factories.ThreadFactory(channel=cls.channel_1, text='Goodbye')
        cls.comment_3 = factories.CommentFactory(author=cls.profile, thread=cls.thread_2, text='bye')
        cls.comment_4 = factories.CommentFactory(thread=cls.thread_2, text='thanks')

        cls.channel_2 = factories.ChannelFactory(workspace=cls.workspace)
        cls.thread_3 = factories.ThreadFactory(channel=cls.channel_2, text='bye')
        cls.comment_5 = factories.CommentFactory(thread=cls.thread_3, text='1234')
        cls.comment_6 = factories.CommentFactory(thread=cls.thread_3, text='heLlo')

    def setUp(self) -> None:
        self.client.force_authenticate(self.profile.user)

    def test_search_by_text(self):
        response = self.client.post(path=self.url, data={'search_string': 'bye'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        self.assertEqual(len(results), 3)

    def test_search_by_text_and_author(self):
        response = self.client.post(path=self.url, data={'search_string': 'llo', 'author': self.profile.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()
        self.assertEqual(len(results), 1)


