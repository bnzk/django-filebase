# -*- coding: utf-8 -*-

from django.conf import settings


# for the future
class FilebaseMultiUploadInlineMixin():

    class Media:
        js = (
            conf.STATIC_URL + 'js/jquery.filebase_multiupload.js',
        )
