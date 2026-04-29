from django.db import models
from music.models import Music
# Create your models here.


class Playlist(models.Model):
    name = models.CharField(max_length=20)
    musics = models.ManyToManyField(Music,related_name='playlists')