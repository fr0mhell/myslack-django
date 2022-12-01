from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from myslack import models, factories


class WorkspaceAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = cls.client_class()
        cls.user = factories.UserFactory()
        cls.workspace_1 = factories.WorkspaceFactory()
        cls.workspace_2 = factories.WorkspaceFactory()
        cls.workspace_3 = factories.WorkspaceFactory()
        cls.profile_1 = factories.ProfileFactory(user=cls.user, workspace=cls.workspace_1)
        cls.profile_2 = factories.ProfileFactory(user=cls.user, workspace=cls.workspace_2)

    def setUp(self) -> None:
        self.client.force_authenticate(self.user)

    def test_list_has_only_user_workspaces(self):
        """Check Workspaces LIST API returns only Workspaces where a User has Profile."""
        response = self.client.get(reverse('myslack:workspaces-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_detail_workspace_wo_profile_not_found(self):
        """Check API responds with 404 when trying to get Workspace where a User does not have profile."""
        response = self.client.get(reverse('myslack:workspaces-detail', args=[self.workspace_3.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


