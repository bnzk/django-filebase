from __future__ import unicode_literals
import json

from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.forms.models import modelform_factory

from filebase import conf
from filebase.admin.filters import FileTypeFilter
from filebase.utils import handle_upload, get_valid_filename, UploadException, sha1_from_file
from filebase.models import File
from filebase.forms import FileAdminChangeFrom


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = [
        'thumb_list', 'label', 'references_list', 'uploader', 'created',
        'modified', ]
    list_filter = [
        FileTypeFilter, 'created', 'modified', 'extension', 'uploader', ]
    list_display_links = ['label', ]
    readonly_fields = [
        'type', 'extension', 'uploader', 'created',
        'modified', 'file_hash', ]
    search_fields = ['filename', 'name', ]

    form = FileAdminChangeFrom

    class Media:
        vendor_path = conf.STATIC_URL + 'js/vendor/'
        js_path = conf.STATIC_URL + 'js/'
        js = (
            vendor_path + 'uppy/uppy.min.js',
            js_path + 'filebase_changelist.js',
        )
        css = {
            'screen': (
                conf.STATIC_URL + 'css/filebase.css',
            )
        }

    # TODO: what if used outside of ADMIN?
    def save_model(self, request, obj, form, change):
        if not change:
            obj.uploader = request.user
            obj.save()
        super(FileAdmin, self).save_model(request, obj, form, change)

    def get_urls(self):
        from django.conf.urls import url
        urls = super(FileAdmin, self).get_urls()

        url_patterns = [
            url(
                r'^ajax-upload/$',
                self.admin_site.admin_view(self.ajax_upload),
                name='filebase-ajax_upload'
            ),
            url(
                r'^ajax-info/$',
                self.admin_site.admin_view(self.ajax_info),
                name='filebase-ajax_info'
            ),
        ]
        url_patterns.extend(urls)
        return url_patterns

    def ajax_info(self, request):
        file_id = request.GET.get("file_id", None)
        file_obj = get_object_or_404(File, pk=file_id)
        mimetype = "application/json" if request.is_ajax() else "text/html"
        response_params = {'content_type': mimetype}
        return HttpResponse(json.dumps(file_obj.get_json_response()),
                            **response_params)

    def ajax_upload(self, request):
        """
        receives an upload from the uploader.
        Receives only one file at the time.
        """
        mimetype = "application/json" if request.is_ajax() else "text/html"
        content_type_key = 'content_type'
        # 'mimetype' if DJANGO_1_4 else 'content_type'
        response_params = {content_type_key: mimetype}

        try:
            upload, filename, is_raw = handle_upload(request)
            FileForm = modelform_factory(
                model=File, fields=('filename', 'file_hash', 'uploader', 'file'))
            uploadform = FileForm(
                {
                    'filename': get_valid_filename(filename),
                    'file_hash': sha1_from_file(upload),
                    'uploader': request.user.pk
                },
                {'file': upload}
            )

            if uploadform.is_valid():
                file_obj = uploadform.save(commit=False)
                file_obj.save()
                json_response = file_obj.get_json_response()
                return HttpResponse(
                    json.dumps(json_response), **response_params)
            else:
                return HttpResponse(
                    json.dumps({
                        'success': False,
                        'message': _(u"Duplicate detected: File with same contents or same name (%(filename)s) already exists. File was not uploaded.") % {'filename': filename, },
                        'errors': uploadform.errors
                    }),
                    status=409,  # conflict
                    **response_params)
        except UploadException as e:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'message': str(e)
                }),
                **response_params)
