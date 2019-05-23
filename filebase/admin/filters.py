from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from filebase import conf
from filebase.models import File


class FileTypeFilter(admin.SimpleListFilter):
    title = _('Type')
    parameter_name = 'type__exact'

    def lookups(self, request, model_admin):
        # TODO: limit filter to existing types?
        # distinct ON doesnt work in sqlite3...soo...
        types = []

        for key, definition in conf.FILE_TYPES.items():
            types.append((key, definition.get("title")))

        return sorted(types, key=lambda type: type[1])

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(type__exact=self.value())
        else:
            return queryset
