import random

from django.core.management.base import BaseCommand

from myslack import factories, models

USER = 1_000
WORKSPACES = 5
CHANNELS = 20
THREADS_MIN = 10
THREADS_MAX = 100
COMMENTS_MIN = 0
COMMENTS_MAX = 20
REACTIONS_MIN = 0
REACTIONS_MAX = 100


class Command(BaseCommand):
    """Custom `filldb` command.
    Django commands docs:
    https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/
    """
    help = 'Fill DB with sample data'

    def handle(self, *args, **options):
        users = factories.UserFactory.create_batch(size=USER)
        workspaces = factories.WorkspaceFactory.create_batch(size=WORKSPACES)

        # Every user has profile in at least 1 Workspace
        for user in users:
            random.shuffle(workspaces)
            for workspace in workspaces:
                factories.ProfileFactory.create(user=user, workspace=workspace)

        for workspace in workspaces:
            channels = factories.ChannelFactory.create_batch(size=CHANNELS, workspace=workspace)
            profiles_qs = models.Profile.objects.filter(workspace_id=workspace)
            profiles_number = profiles_qs.count()

            for channel in channels:
                profiles = random.sample(profiles_qs, random.randint(profiles_number // 10, profiles_number))

                for profile in profiles:
                    factories.ChannelMembershipFactory.create(profile=profile, channel=channel)

                # Create threads in channel

                # Add comments to every thread

                # Add reactions to threads and comments
