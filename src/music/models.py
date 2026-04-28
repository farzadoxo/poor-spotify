from django.db import models



class Music(models.Model):
    fileName = models.CharField(max_length=50,null=False)
    title = models.CharField(max_length=50,null=True)
    artist = models.CharField(max_length=30,null=True)
    isSingleTrack = models.BooleanField(null=True,default=None)
    album = models.CharField(max_length=30,null=True)
    hasCover = models.BooleanField(default=True,null=True)
    coverFormat = models.CharField(max_length=5,null=True)
    url = models.CharField(max_length=10,unique=True)
    format = models.CharField(max_length=5)
    uploader = models.CharField(max_length=30,null=False)