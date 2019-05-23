from django.contrib import admin

from filebase.models import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):

    def get_model_perms(self, request):
        """
        It seems this is only used for the list view. NICE :-)
        """
        return {
            'add': False,
            'change': False,
            'delete': False,
        }