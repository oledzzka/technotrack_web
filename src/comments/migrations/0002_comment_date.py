# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
