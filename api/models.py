from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MusicStyle(models.TextChoices):
    ELECTRO = 'electro'


class Album(models.Model):
    title = models.TextField()
    added_on = models.DateField(auto_now=True)
    date = models.DateField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums', editable=False)


class Sound(models.Model):
    title = models.TextField()
    style = models.CharField(choices=MusicStyle.choices, max_length=0x100)
    file = models.FileField()
    added_on = models.DateField(auto_now=True, editable=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='sounds', null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sounds', editable=False)


class Playlist(models.Model):
    title = models.TextField()
    added_on = models.DateField(auto_now=True)
    sounds = models.ManyToManyField(Sound)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', editable=False)
