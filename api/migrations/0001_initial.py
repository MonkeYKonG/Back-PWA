# Generated by Django 3.1.7 on 2021-03-11 13:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('added_on', models.DateField(auto_now=True)),
                ('date', models.DateField()),
                ('picture', models.FileField(null=True, upload_to='')),
                ('added_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='albums', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MusicStyles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('added_on', models.DateField(auto_now=True)),
                ('added_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('file', models.FileField(upload_to='')),
                ('added_on', models.DateField(auto_now=True)),
                ('added_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='sounds', to=settings.AUTH_USER_MODEL)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sounds', to='api.album')),
                ('artist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sounds', to='api.artist')),
                ('style', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.musicstyles')),
            ],
        ),
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='user_followed', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SoundLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='sound_likes', to=settings.AUTH_USER_MODEL)),
                ('sound', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='likers', to='api.sound')),
            ],
        ),
        migrations.CreateModel(
            name='SoundComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('post_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='sound_comments', to=settings.AUTH_USER_MODEL)),
                ('sound', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.sound')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfilePicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.FileField(null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_picture', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileNotificationSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=512)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notification_subscription', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='playlist_likes', to=settings.AUTH_USER_MODEL)),
                ('playlist', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='likers', to='api.playlist')),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistFollowing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='playlist_followed', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='api.playlist')),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.playlist')),
                ('post_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='playlist_comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='playlist',
            name='sounds',
            field=models.ManyToManyField(to='api.Sound'),
        ),
    ]
