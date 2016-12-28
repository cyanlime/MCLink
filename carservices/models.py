from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Account(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    carmeid = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    def __unicode__(self):
        return self.carmeid

class WXUser(models.Model):
    openid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    head_portrait = models.URLField()
    account = models.ForeignKey('Account', blank=True, null=True, on_delete=models.SET_NULL)
    bind = models.BooleanField()
    def __unicode__(self):
        return self.openid

class Position(models.Model):
    account = models.ForeignKey('Account')
    longitude = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    bearing = models.CharField(max_length=200)
    speed = models.CharField(max_length=200)
    time = models.DateTimeField()
    def __unicode__(self):
        return self.account.carmeid