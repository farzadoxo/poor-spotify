from django.db import models



class Music(models.Model):
    fileName = models.CharField(max_length=50,null=True)
    title = models.CharField(max_length=50,null=False)
    artist = models.CharField(max_length=30,null=False)
    isSingleTrack = models.BooleanField(null=False,default=None)
    album = models.CharField(max_length=30,null=False)
    hasCover = models.BooleanField(default=True,null=True)
    coverFormat = models.CharField(max_length=5,null=False)
    url = models.CharField(max_length=10,unique=False)
    format = models.CharField(max_length=5)
    uploader = models.CharField(max_length=30,null=False)