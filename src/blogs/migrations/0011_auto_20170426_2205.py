# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-26 22:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0010_auto_20170426_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
