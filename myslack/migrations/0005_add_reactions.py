from django.db import migrations

from myslack.constants import REACTION_SLUGS


def add_reactions(apps, schema_editor):
    Reaction = apps.get_model('myslack', 'Reaction')
    Reaction.objects.bulk_create([Reaction(slug=reaction_slug) for reaction_slug in REACTION_SLUGS])


class Migration(migrations.Migration):

    dependencies = [
        ('myslack', '0004_comment_author_thread_author_alter_thread_channel'),
    ]

    operations = [
        migrations.RunPython(add_reactions),
    ]
