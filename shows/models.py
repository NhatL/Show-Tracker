from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Episode(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(default=1, unique=True)
    season = models.ForeignKey("Season")
    description = models.TextField(null=True, blank=True, default="")
    movie_db_id = models.IntegerField(null=True, blank=True)


class Season(models.Model):
    number = models.IntegerField(default=1, unique=True)
    movie_db_id = models.IntegerField(null=True, blank=True)
    show = models.ForeignKey("Show")

    def __unicode__(self):
        return self.show.name + ": S%02d" % (self.number, )


class Show(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    ongoing = models.BooleanField(default=True)
    movie_db_id = models.IntegerField(null=True, blank=True)
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)
    movie_db_id = models.IntegerField(null=True, blank=True)
    show = models.ManyToManyField(Show)

    def __unicode__(self):
        return self.name
