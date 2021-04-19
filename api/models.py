from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_picture')
    picture = models.FileField(null=True)


class Album(models.Model):
    title = models.TextField()
    picture = models.FileField(null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')


class Artist(models.Model):
    name = models.CharField(max_length=0x100, unique=True)


class MusicStyle(models.Model):
    name = models.CharField(max_length=0x100, unique=True)


class Sound(models.Model):
    title = models.TextField()
    style = models.ForeignKey(MusicStyle, on_delete=models.CASCADE)
    file = models.FileField()
    added_on = models.DateField(auto_now=True, editable=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='sounds', null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sounds', editable=False)


class Playlist(models.Model):
    title = models.TextField()
    added_on = models.DateField(auto_now=True, editable=False)
    sounds = models.ManyToManyField(Sound)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', editable=False)


class BaseComment(models.Model):
    added_on = models.DateTimeField(auto_now=True, editable=False)
    message = models.TextField()

    class Meta:
        abstract = True


class SoundComment(BaseComment):
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE, related_name='comments', editable=False)
    post_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sound_comments', editable=False)


class PlaylistComment(BaseComment):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='comments', editable=False)
    post_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlist_comments', editable=False)


class UserFollowing(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_followed', editable=False)
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', editable=False)


class PlaylistFollowing(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlist_followed', editable=False)
    target = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='followers', editable=False)


class SoundLike(models.Model):
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE, related_name='likers', editable=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sound_likes', editable=False)


class PlaylistLike(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='likers', editable=False)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlist_likes', editable=False)
