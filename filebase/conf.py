from django.conf import settings as settings
from django.core.files.storage import DefaultStorage
from django.utils.translation import ugettext_lazy as _


def _get_or_default(local_setting_name, setting_default):
    global_setting_name = 'FILEBASE_{}'.format(local_setting_name)
    setting_value = getattr(
        settings,
        global_setting_name,
        setting_default,
    )
    globals()[local_setting_name] = setting_value
    if not getattr(settings, global_setting_name, None):
        setattr(settings, global_setting_name, setting_value)

# where to store files
_get_or_default('FILE_STORAGE', DefaultStorage())


# where to store thumbnails
_get_or_default('THUMBNAIL_STORAGE', DefaultStorage())


# upload to (within storage). can be a callable
_get_or_default('UPLOAD_TO', 'files')


# put thumbnails in (within its storage). can be a callable
_get_or_default('THUMBNAIL_TO', 'thumbs')


# thumb sizes
_get_or_default('IMAGE_SIZES', {
        'LIST': (100, 70),
        'FIELD': (220, 150),
    }
)


# just because?
_get_or_default('STATIC_URL', settings.STATIC_URL + "filebase/")


# file types
_get_or_default('FILE_TYPES', {
        'image': {
            'title': _(u'Image'),
            'extensions': ('jpg', 'jpeg', 'png', 'gif', 'tif', 'tiff', ),
        },
        'video': {
            'title': _(u'Video'),
            'extensions': ('mp4', 'avi', 'mkv', 'ogg', 'wma', 'mov'),
        },
        'pdf': {
            'title': _(u'PDF document'),
            'extensions': ('pdf'),
        },
        'flash': {
            'title': _(u'Flash'),
            'extensions': ('swf', 'fla', 'as3'),
        },
        'archive': {
            'title': _(u'Archive (zip, etc)'),
            'extensions': ('tgz', 'gzip', 'gz', 'zip', 'tar', 'rar'),
        },
        'audio': {
            'title': _(u'Audio'),
            'extensions': ('mp3', 'wav', 'aac', 'aiff', 'flac'),
        },
        'document': {
            'title': _(u'Text document'),
            'extensions': ('odt', 'doc', 'docx', 'rtf'),
        },
        'spreadsheet': {
            'title': _(u'Spreadsheet'),
            'extensions': ('ods', 'xlsx', 'xls', ),
        },
        'presentation': {
            'title': _(u'Presentation'),
            'extensions': ('ppt', 'pptx', 'odp'),
        },
    }
)

#
# class FilebaseConf(AppConf):
#
#     class Meta:
#         proxy = True
#
#     DEBUG = False
#     # could have custom
#     FILE_STORAGE = DefaultStorage()
#     # could have custom
#     THUMBNAIL_STORAGE = DefaultStorage()
#     # base upload path
#     UPLOAD_TO = 'files'
#     # base thumbnails path
#     THUMBNAIL_TO = 'thumbs'
#     # convenience
#     STATIC_URL = django_settings.STATIC_URL + "filebase/"
#     # Image?
#     FILE_TYPES = {
#         'image': {
#             'title': _(u'Image'),
#             'extensions': ('jpg', 'jpeg', 'png', 'gif', 'tif', 'tiff', ),
#         },
#         'video': {
#             'title': _(u'Video'),
#             'extensions': ('mp4', 'avi', 'mkv', 'ogg', 'wma', 'mov'),
#         },
#         'pdf': {
#             'title': _(u'PDF document'),
#             'extensions': ('pdf'),
#         },
#         'flash': {
#             'title': _(u'Flash'),
#             'extensions': ('swf', 'fla', 'as3'),
#         },
#         'archive': {
#             'title': _(u'Archive (zip, etc)'),
#             'extensions': ('tgz', 'gzip', 'gz', 'zip', 'tar', 'rar'),
#         },
#         'audio': {
#             'title': _(u'Audio'),
#             'extensions': ('mp3', 'wav', 'aac', 'aiff', 'flac'),
#         },
#         'document': {
#             'title': _(u'Text document'),
#             'extensions': ('odt', 'doc', 'docx', 'rtf'),
#         },
#         'spreadsheet': {
#             'title': _(u'Spreadsheet'),
#             'extensions': ('ods', 'xlsx', 'xls', ),
#         },
#         'presentation': {
#             'title': _(u'Presentation'),
#             'extensions': ('ppt', 'pptx', 'odp'),
#         },
#     }
#     IMAGE_WIDTH_LIST = '150'
#     IMAGE_HEIGHT_LIST = '150'
#     IMAGE_WIDTH_FIELD = '200'
#     IMAGE_HEIGHT_FIELD = '150'
