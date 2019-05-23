# coding: utf-8

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Folder(models.Model):
    parent = models.ForeignKey(
        'filebase.Folder',
        null=True,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        verbose_name=_("parent")
    )
    name = models.CharField(
        max_length=32,
        verbose_name=_('name'),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created'),
    )

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _(u'Folder')
        verbose_name_plural = _(u'Folders')

    @property
    def children(self):
        return self.folder_set.all()

    @property
    def files(self):
        return self.file_set.all()
