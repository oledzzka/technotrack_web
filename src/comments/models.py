from __future__ import unicode_literals

from django.db import models
from blogs.models import Post
from core.models import User

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(User, related_name='comments')
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)