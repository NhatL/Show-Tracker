# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-06 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0003_auto_20161006_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='movie_db_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='genre',
            name='movie_db_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='season',
            name='movie_db_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='movie_db_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
