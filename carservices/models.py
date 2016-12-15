from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Account(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    def __unicode__(self):
        return self.id

class WXUser(models.Model):
    openid = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    head_portrait = models.URLField()
    account = models.ForeignKey('Account', blank=True, null=True, on_delete=models.SET_NULL)
    def __unicode__(self):
        return self.openid