# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-17 12:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('number', models.IntegerField(default=1)),
                ('air_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('movie_db_id', models.IntegerField(blank=True, null=True)),
                ('server_img_path', models.CharField(blank=True, max_length=255, null=True)),
                ('local_img_path', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('movie_db_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('movie_db_id', models.IntegerField(default=1)),
                ('server_img_path', models.CharField(blank=True, max_length=255, null=True)),
                ('local_img_path', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('popularity', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.TextField(blank=True, default='', null=True)),
                ('ongoing', models.BooleanField(default=True)),
                ('movie_db_id', models.IntegerField(blank=True, default=1, null=True)),
                ('episode_count', models.IntegerField(blank=True, default=1, null=True)),
                ('last_updated', models.DateField(blank=True, null=True)),
                ('first_air', models.DateField(blank=True, null=True)),
                ('vote_average', models.CharField(blank=True, max_length=30, null=True)),
                ('vote_count', models.CharField(blank=True, max_length=30, null=True)),
                ('server_img_path', models.CharField(blank=True, max_length=255, null=True)),
                ('local_img_path', models.CharField(blank=True, max_length=255, null=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('watched_episodes', models.ManyToManyField(to='shows.Episode')),
            ],
        ),
        migrations.AddField(
            model_name='season',
            name='show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.Show'),
        ),
        migrations.AddField(
            model_name='genre',
            name='show',
            field=models.ManyToManyField(to='shows.Show'),
        ),
        migrations.AddField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shows.Season'),
        ),
    ]
