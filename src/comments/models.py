# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from blogs.models import Post
from django.conf import settings

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments')
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = u'Коментарий'
        verbose_name_plural = u'Коментарии'
        ordering = ('date',)