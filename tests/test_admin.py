# -*- coding: utf-8 -*-

# from django.forms.models import modelform_factory
import os
import json

from django.test import TestCase
from django.conf import settings
from django.urls import reverse

from filebase.models import File
from .utils import create_superuser, create_image


class filebaseAdminUrlsTests(TestCase):

    def setUp(self):
        self.superuser = create_superuser()
        self.client.login(username='admin', password='secret')
        self.img = create_image()
        self.image_name = 'test_file.jpg'
        self.filename = os.path.join(settings.FILE_UPLOAD_TEMP_DIR,
                                     self.image_name)
        self.img.save(self.filename, 'JPEG')

    def tearDown(self):
        self.client.logout()

    def test_app_index_get(self):
        response = self.client.get(reverse('admin:app_list', args=('filebase',)))
        self.assertEqual(response.status_code, 200)

    def test_file_change_list(self):
        # upload file, so we get an item in the list
        self.client.post(
            reverse('admin:filebase-ajax_upload'),
            {'ajax_file': open(self.filename, 'rb'), }
        )
        response = self.client.get(reverse('admin:filebase_file_changelist'))
        self.assertEqual(response.status_code, 200)

    def test_file_change_view(self):
        self.client.post(
            reverse('admin:filebase-ajax_upload'),
            {'ajax_file': open(self.filename, 'rb'), }
        )
        file_id = File.objects.all()[0].id
        response = self.client.get(reverse('admin:filebase_file_change', args=(file_id, )))
        self.assertEqual(response.status_code, 200)

    def test_empty_file_field(self):
        response = self.client.get(reverse('admin:test_app_testmodel_add'))
        self.assertEqual(response.status_code, 200)

    def test_file_upload(self):
        self.assertEqual(File.objects.count(), 0)
        self.client.post(
            reverse('admin:filebase-ajax_upload'),
            {'ajax_file': open(self.filename, 'rb'), }
        )
        self.assertEqual(File.objects.count(), 1)

    def test_bad_file_upload(self):
        self.assertEqual(File.objects.count(), 0)
        response = self.client.post(
            reverse('admin:filebase-ajax_upload'), {}
        )
        # decode, for python 3.5!?
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data["success"], False)

    def test_non_post_upload_request(self):
        self.assertEqual(File.objects.count(), 0)
        response = self.client.get(reverse('admin:filebase-ajax_upload'))
        # decode, for python 3.5!?
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data["success"], False)

    def test_prevent_duplicate_file_name_upload(self):
        self.assertEqual(File.objects.count(), 0)
        self.client.post(
            reverse('admin:filebase-ajax_upload'),
            {'ajax_file': open(self.filename, 'rb'), }
        )
        self.assertEqual(File.objects.count(), 1)
        response = self.client.post(
            reverse('admin:filebase-ajax_upload'),
            {'ajax_file': open(self.filename, 'rb'), }
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(File.objects.count(), 1)

    def test_prevent_duplicate_file_content_upload(self):
        self.assertEqual(File.objects.count(), 0)
        self.client.post(
            reverse('admin:filebase-ajax_upload'),
            {'ajax_file': open(self.filename, 'rb'), 'filename': "first-%s" % self.image_name}
        )
        self.assertEqual(File.objects.count(), 1)
        response = self.client.post(
            reverse('admin:filebase-ajax_upload'),
            {'ajax_file': open(self.filename, 'rb'), 'filename': "second-%s" % self.image_name}
        )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(File.objects.count(), 1)

    def test_prevent_duplicate_json_response(self):
        self.assertEqual(File.objects.count(), 0)
        self.client.post(
            reverse('admin:filebase-ajax_upload'),
            {'ajax_file': open(self.filename, 'rb'), 'filename': "first-{}".format(self.image_name), }
        )
        self.assertEqual(File.objects.count(), 1)
        response = self.client.post(
            reverse('admin:filebase-ajax_upload'),
            {'ajax_file': open(self.filename, 'rb'), 'filename': "second-{}".format(self.image_name)}
        )
        # decode, for python 3.5!?
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data["success"], False)
        self.assertGreaterEqual(len(data["errors"]), 1)
