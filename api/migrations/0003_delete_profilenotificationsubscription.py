# Generated by Django 3.2 on 2021-04-14 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_sound_artist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProfileNotificationSubscription',
        ),
    ]
