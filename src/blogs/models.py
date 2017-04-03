# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'
    def __unicode__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog')
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    description = models.TextField(default='')
    category = models.ManyToManyField(Category,related_name='blog')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Блог'
        verbose_name_plural = u'Блоги'
        ordering = ('-date',)

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    blog = models.ForeignKey(Blog, related_name='posts')
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'Пост'
        verbose_name_plural = u'Посты'
        ordering = ('-date',)
