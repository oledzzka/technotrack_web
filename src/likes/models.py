from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.

class Like(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='like')
    date = models.DateField()