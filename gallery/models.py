# coding: utf-8
# Copyright (c) 2011 Aymeric Augustin. All rights reserved.

import hashlib
import os

from django.conf import settings
from django.db import models

from .imgutil import make_thumbnail

class Album(models.Model):
    dirpath = models.CharField(max_length=200, unique=True,
            verbose_name="directory path")
    date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ('-date', 'dirpath')

    def __unicode__(self):
        return self.name or self.dirpath

    @models.permalink
    def get_absolute_url(self):
        return 'gallery-album', [self.pk]


class Photo(models.Model):
    album = models.ForeignKey(Album)
    filename = models.CharField(max_length=100,
        verbose_name="file name")
    date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('date', 'filename')
        unique_together = ('album', 'filename')

    def __unicode__(self):
        return self.filename

    @models.permalink
    def get_absolute_url(self):
        return 'gallery-photo', [self.album.pk, self.pk]

    def abspath(self):
        return os.path.join(settings.PHOTO_ROOT, self.album.dirpath, self.filename)

    def thumbname(self, preset):
        ext = os.path.splitext(self.filename)[1]
        hsh = hashlib.sha1()
        hsh.update(self.album.dirpath)
        hsh.update(self.filename)
        hsh.update(str(settings.PHOTO_RESIZE_PRESETS[preset]))
        return hsh.hexdigest() + ext

    def thumbnail(self, preset):
        thumbpath = os.path.join(settings.PHOTO_CACHE, self.thumbname(preset))
        if not os.path.exists(thumbpath):
            make_thumbnail(self.abspath(), thumbpath, preset)
        return thumbpath



