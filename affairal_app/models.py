from __future__ import unicode_literals

from django import forms
from django.db import models
from django.contrib.auth.models import User

import uuid


# Create your models here
class AffairalUser(models.Model):

    user = models.OneToOneField(User, primary_key=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    reg_id = models.TextField(default=uuid.uuid4())
    tickets_count = models.IntegerField(default=1)
    name = models.TextField(null=True)
    mobile = models.TextField(null=True)
    reg_type = models.TextField(default='self')
    document = models.FileField(upload_to='documents/')
    install_ts = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    update_ts = models.DateTimeField(auto_now=True, null=False, blank=True)

    def __unicode__(self):
        return (self.name)

    def image_img(self):
        if self.document:
            return u'<img src="%s" width="50" height="50" />' % self.document.url
        else:
            return '(Sin imagen)'

    image_img.short_description = 'Thumb'
    image_img.allow_tags = True


class UserDocument(models.Model):

    owner = models.ForeignKey('auth.User', related_name='documents')
    title = models.TextField(null=True)
    file = models.FileField(upload_to='documents/')
    install_ts = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    update_ts = models.DateTimeField(auto_now=True, null=False, blank=True)


class Event(models.Model):

    owner = models.ForeignKey('auth.User', related_name='events')
    name = models.TextField()
    event_type = models.TextField()
    location = models.TextField()
    is_notified = models.BooleanField(default=False)
    remind_before = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    install_ts = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    update_ts = models.DateTimeField(auto_now=True, null=False, blank=True)
