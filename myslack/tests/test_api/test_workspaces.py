from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from myslack import factories

fake = Faker()
Faker.seed(0)


class WorkspaceAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = cls.client_class()
        cls.user = factories.UserFactory()
        cls.workspace_1 = factories.WorkspaceFactory()
        cls.workspace_2 = factories.WorkspaceFactory()
        cls.workspace_3 = factories.WorkspaceFactory()
        cls.profile_1 = factories.ProfileFactory(user=cls.user, workspace=cls.workspace_1, is_workspace_admin=True)
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

    def test_invite_not_workspace_admin_not_allowed(self):
        self.profile_1.is_workspace_admin = False
        self.profile_1.save()
        response = self.client.post(
            path=reverse('myslack:workspaces-invite-by-email', args=[self.workspace_1.id]),
            data={'email': fake.ascii_email()},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite(self):
        response = self.client.post(
            path=reverse('myslack:workspaces-invite-by-email', args=[self.workspace_1.id]),
            data={'email': fake.ascii_email()},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invite_user_from_another_workspace(self):
        profile = factories.ProfileFactory(workspace=self.workspace_2)

        response = self.client.post(
            path=reverse('myslack:workspaces-invite-by-email', args=[self.workspace_1.id]),
            data={'email': profile.user.email},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invite_existent_profile_cannot_be_invited_again(self):
        profile = factories.ProfileFactory(workspace=self.workspace_1)

        response = self.client.post(
            path=reverse('myslack:workspaces-invite-by-email', args=[self.workspace_1.id]),
            data={'email': profile.user.email},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error = response.json()['non_field_errors'][0]
        self.assertEqual(error, f'Profile for email "{profile.user.email}" already exists')


class ProfileAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = cls.client_class()
        cls.workspace_1 = factories.WorkspaceFactory()
        cls.workspace_2 = factories.WorkspaceFactory()
        cls.profile_1 = factories.ProfileFactory(workspace=cls.workspace_1)
        cls.admin_profile_1 = factories.ProfileFactory(workspace=cls.workspace_1, is_workspace_admin=True)
        cls.profile_2 = factories.ProfileFactory(workspace=cls.workspace_2)

    def setUp(self) -> None:
        self.client.force_authenticate(self.profile_1.user)

    def test_list_only_workspace_profiles(self):
        response = self.client.get(path=reverse('myslack:profiles-list', args=[self.workspace_1.id]))
        results = response.json()['results']
        self.assertEqual(len(results), 2)
        result_profile_ids = {res['id'] for res in results}
        self.assertSetEqual(result_profile_ids, {self.profile_1.id, self.admin_profile_1.id})

    def test_update_not_workspace_admin_forbidden(self):
        response = self.client.put(
            path=reverse('myslack:profiles-detail', args=[self.workspace_1.id, self.profile_1.id]),
            data={'display_name': 'New display name'},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_workspace_admin_allowed_to_edit_any_workspace_profile(self):
        self.client.force_authenticate(self.admin_profile_1.user)

        for profile in [self.profile_1, self.admin_profile_1]:
            with self.subTest(profile=profile):
                response = self.client.patch(
                    path=reverse('myslack:profiles-detail', args=[self.workspace_1.id, profile.id]),
                    data={'display_name': 'New display name'},
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                profile.refresh_from_db()
                self.assertEqual(profile.display_name, 'New display name')

    def test_my_profile_get(self):
        response = self.client.get(path=reverse('myslack:profiles-my-profile', args=[self.workspace_1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.profile_1.id)

    def test_my_profile_patch(self):
        response = self.client.patch(
            path=reverse('myslack:profiles-my-profile', args=[self.workspace_1.id]),
            data={'display_name': 'New display name'},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile_1.refresh_from_db()
        self.assertEqual(response.json()['display_name'], self.profile_1.display_name)
