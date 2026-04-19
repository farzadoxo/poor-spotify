from django.db import models



class Music(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=10)
    format = models.CharField(max_length=5)