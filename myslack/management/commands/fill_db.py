import random

from django.core.management.base import BaseCommand

from myslack import factories, models

USER = 200
WORKSPACES = 5
CHANNELS = 10
THREADS_MIN = 5
THREADS_MAX = 15
COMMENTS_MIN = 1
COMMENTS_MAX = 20
REACTIONS_MIN = 1
REACTIONS_MAX = 25


class Command(BaseCommand):
    """Custom `filldb` command.
    Django commands docs:
    https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/
    """
    help = 'Fill DB with sample data'

    def handle(self, *args, **options):
        print('Creating Users...')
        users = factories.UserFactory.create_batch(size=USER)
        print('Creating Workspaces...')
        workspaces = factories.WorkspaceFactory.create_batch(size=WORKSPACES)

        # Every user has profile in at least 1 Workspace
        print('Adding Users to Workspaces...')
        for user in users:
            workspaces = random.sample(workspaces, random.randint(1, WORKSPACES))
            for workspace in workspaces:
                factories.ProfileFactory.create(user=user, workspace=workspace)

        print('Adding content to Workspaces...')
        for workspace in workspaces:

            print(f'Filling {workspace}...')
            print('\tAdding channels...')
            channels = factories.ChannelFactory.create_batch(size=CHANNELS, workspace=workspace)
            all_profiles = list(models.Profile.objects.filter(workspace_id=workspace))
            profiles_number = len(all_profiles)

            for channel in channels:

                print(f'\tFilling {channel}...')
                print('\t\tAdding Channel members...')
                profiles = random.sample(all_profiles, random.randint(profiles_number // 2, profiles_number))

                for profile in profiles:
                    factories.ChannelMembershipFactory.create(profile=profile, channel=channel)

                print('\t\tAdding Threads...')
                threads = [
                    factories.ThreadFactory(author=random.choice(profiles), channel=channel)
                    for _ in range(random.randint(THREADS_MIN, THREADS_MAX))
                ]

                print('\t\tAdding Comments to Threads...')
                comments = []
                for thread in threads:
                    comments.extend([
                        factories.CommentFactory(thread=thread, author=random.choice(profiles))
                        for _ in range(random.randint(COMMENTS_MIN, COMMENTS_MAX))
                    ])

                print('\t\tAdding Reactions to Threads...')
                for thread in threads:
                    factories.ThreadReactionFactory(thread=thread, profile=random.choice(profiles))

                print('\t\tAdding Reactions to Comments...')
                for comment in comments:
                    factories.CommentReactionFactory(comment=comment, profile=random.choice(profiles))
