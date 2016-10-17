from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Show(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    popularity = models.CharField(max_length=30, null=True, blank=True)
    description = models.TextField(null=True, blank=True, default="")
    ongoing = models.BooleanField(default=True)
    movie_db_id = models.IntegerField(default=1, null=True, blank=True)
    users = models.ManyToManyField(User)
    episode_count = models.IntegerField(null=True, blank=True, default=1)
    last_updated = models.DateField(null=True, blank=True)
    first_air = models.DateField(null=True, blank=True)
    vote_average = models.CharField(max_length=30, null=True, blank=True)
    vote_count = models.CharField(max_length=30, null=True, blank=True)
    server_img_path = models.CharField(max_length=255, null=True, blank=True)
    local_img_path = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class Season(models.Model):
    number = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True, default="")
    movie_db_id = models.IntegerField(default=1)
    show = models.ForeignKey("Show")
    server_img_path = models.CharField(max_length=255, null=True, blank=True)
    local_img_path = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.show.name + ": S%02d" % (self.number, ))


class Episode(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(default=1)
    air_date = models.DateField(null=True, blank=True)
    season = models.ForeignKey("Season")
    description = models.TextField(null=True, blank=True, default="")
    movie_db_id = models.IntegerField(null=True, blank=True)
    server_img_path = models.CharField(max_length=255, null=True, blank=True)
    local_img_path = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return unicode(unicode(self.season) + "E%02d" % (self.number, ))


class Genre(models.Model):
    name = models.CharField(max_length=255, default='')
    movie_db_id = models.IntegerField(null=True, blank=True)
    show = models.ManyToManyField(Show)

    def __unicode__(self):
        return unicode(self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watched_episodes = models.ManyToManyField(Episode)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
