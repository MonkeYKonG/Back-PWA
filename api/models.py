from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MusicStyle(models.TextChoices):
    ELECTRO = 'electro'


class Playlist(models.Model):
    title = models.TextField()
    added_on = models.DateField(auto_now=True)


class Album(models.Model):
    title = models.TextField()
    added_on = models.DateField(auto_now=True)
    date = models.DateField()


class Sound(models.Model):
    title = models.TextField()
    style = models.CharField(choices=MusicStyle.choices, max_length=0x100)
    file = models.FileField()
    added_on = models.DateField(auto_now=True, editable=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='sounds')
    playlists = models.ManyToManyField(Playlist, related_name='sounds')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sounds')
