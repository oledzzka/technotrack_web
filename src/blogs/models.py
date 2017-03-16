from __future__ import unicode_literals

from django.db import models
from core.models import User

# Create your models here.

class Blog(models.Model):
    author = models.ForeignKey(User, related_name='blog')
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    blog = models.ForeignKey(Blog, related_name='posts')
    date = models.DateTimeField(auto_now=True)