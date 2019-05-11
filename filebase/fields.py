# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
# from django.conf import settings as globalsettings
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.contrib.admin.sites import site
import django
from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from filebase.models import File
from filebase import conf


# compat thing!
if django.VERSION[:2] < (1, 10):
    from django.core.urlresolvers import reverse
else:
    from django.urls import reverse


# this part is mostly inspired by django-filer: https://github.com/stefanfoulis/django-filer/blob/develop/filer/fields/file.py
# uploader basics: https://github.com/blueimp/jQuery-File-Upload/wiki/Basic-plugin
class FilebaseFileWidget(ForeignKeyRawIdWidget):
    choices = None

    def render(self, name, value, attrs=None):
        obj = self.obj_for_value(value)
        if value:
            try:
                File.objects.get(pk=value)
            except Exception:
                if conf.DEBUG:
                    raise

        params = self.url_parameters()
        if params:
            lookup_url = '?' + '&amp;'.join(
                ['%s=%s' % (k, v) for k, v in list(params.items())])
        else:
            lookup_url = ''

        if 'class' not in attrs:
            # The JavaScript looks for this hook.
            attrs['class'] = 'vForeignKeyRawIdAdminField'
        else:
            attrs['class'] += ' vForeignKeyRawIdAdminField'
        # rendering the super for ForeignKeyRawIdWidget on purpose here because
        # we only need the input and none of the other stuff that
        # ForeignKeyRawIdWidget adds
        hidden_input = super(ForeignKeyRawIdWidget, self).render(name, value,
                                                                 attrs)
        css_id = attrs.get('id', 'id_file_x')

        # related_url = reverse('admin:filer-directory_listing-last')
        related_url = reverse('admin:filebase_file_changelist')

        has_svg = True
        if django.VERSION[:2] < (1, 9):
            has_svg = False

        context = {
            'filebase_static': settings.STATIC_URL + "filebase/",
            'admin_static': settings.STATIC_URL + "admin/",
            'hidden_input': hidden_input,
            'lookup_url': '%s%s' % (related_url, lookup_url),
            'object': obj,
            'width': conf.IMAGE_WIDTH_FIELD,
            'height': conf.IMAGE_HEIGHT_FIELD,
            'size': '%sx%s' % (conf.IMAGE_WIDTH_FIELD, conf.IMAGE_HEIGHT_FIELD),
            'id': css_id,
            'name': name,
            'img_search': 'img/search.svg' if has_svg else 'img/selector-search.gif',
            'img_unknown': 'img/icon-unknown.svg' if has_svg else 'img/icon-unknown.gif',
            'img_upload': 'img/icon-addlink.svg' if has_svg else 'img/icon-addlink.gif',
            'img_changelink': 'img/icon-changelink.svg' if has_svg else 'img/icon-changelink.gif',
            'img_deletelink': 'img/icon-deletelink.svg' if has_svg else 'img/icon-deletelink.gif',
        }
        html = render_to_string('admin/filebase/file_widget.html', context)
        return mark_safe(html)

    def label_for_value(self, value):
        obj = self.obj_for_value(value)
        return '&nbsp;<strong>%s</strong>' % obj

    def obj_for_value(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            value = 0
        try:
            # key = self.rel.get_related_field().name
            # obj = self.rel.to._default_manager.get(**{key: value})
            # we know it's a File!
            obj = File.objects.get(pk=value)
        except File.DoesNotExist:
            obj = None
        return obj

    class Media:
        js = (
            # 'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            # conf.STATIC_URL + 'js/vendor/jquery-1.9.1.min.js',
            conf.STATIC_URL + 'js/jquery_pre_init.js',  # for the moment!
            conf.STATIC_URL + 'js/vendor/jquery.ui.widget.js',
            conf.STATIC_URL + 'js/vendor/jquery.iframe-transport.js',
            conf.STATIC_URL + 'js/vendor/jquery.fileupload.js',
            conf.STATIC_URL + 'js/jquery.filebase_file_widget.js',
            conf.STATIC_URL + 'js/popup_handling.js',  # in popup, we call "opener.dismisss....
            conf.STATIC_URL + 'js/jquery.filebase_widget_init.js',
            conf.STATIC_URL + 'js/jquery_post_init.js',  # for the moment!
        )
        css = {
            'screen': (conf.STATIC_URL + "css/filebase.css", )
        }


class FilebaseFileFormField(forms.ModelChoiceField):
    widget = FilebaseFileWidget

    def __init__(self, rel, queryset, to_field_name, *args, **kwargs):
        self.rel = rel
        self.queryset = queryset
        self.limit_choices_to = kwargs.pop("limit_choices_to", {})
        self.to_field_name = to_field_name
        self.max_value = None
        self.min_value = None
        kwargs.pop('widget', None)
        forms.Field.__init__(self, widget=self.widget(rel, site), *args, **kwargs)

    def widget_attrs(self, widget):
        widget.required = self.required
        return {}


class FilebaseFileField(models.ForeignKey):
    default_form_class = FilebaseFileFormField
    default_model_class = File

    def __init__(self, **kwargs):
        if "on_delete" not in kwargs:
            # protect yourself
            kwargs['on_delete'] = models.PROTECT
        if "to" not in kwargs:
            kwargs['to'] = self.default_model_class
        return super(FilebaseFileField, self).__init__(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(FilebaseFileField, self).deconstruct()
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {
            'form_class': self.default_form_class,
            'rel': self.rel if hasattr(self, 'rel') else self.remote_field,
        }
        defaults.update(kwargs)
        return super(FilebaseFileField, self).formfield(**defaults)

    # def south_field_triple(self):
    #     "Returns a suitable description of this field for South."
    #     # We'll just introspect ourselves, since we inherit.
    #     from south.modelsinspector import introspector
    #     field_class = "django.db.models.fields.related.ForeignKey"
    #     args, kwargs = introspector(self)
    #     # That's our definition!
    #     return (field_class, args, kwargs)
