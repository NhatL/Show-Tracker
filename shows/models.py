from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Show(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    popularity = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True, default="")
    ongoing = models.BooleanField(default=True)
    movie_db_id = models.IntegerField(default=1, null=True, blank=True)
    users = models.ManyToManyField(User)
    last_updated = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class Season(models.Model):
    number = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True, default="")
    movie_db_id = models.IntegerField(default=1)
    show = models.ForeignKey("Show")

    def __unicode__(self):
        return unicode(self.show.name + ": S%02d" % (self.number, ))


class Episode(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(default=1)
    air_date = models.DateField(null=True, blank=True)
    season = models.ForeignKey("Season")
    description = models.TextField(null=True, blank=True, default="")
    movie_db_id = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return unicode(unicode(self.season) + "E%02d" % (self.number, ))


class Genre(models.Model):
    name = models.CharField(max_length=255, default='')
    movie_db_id = models.IntegerField(null=True, blank=True)
    show = models.ManyToManyField(Show)

    def __unicode__(self):
        return unicode(self.name)
