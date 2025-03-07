import base64
from audioop import reverse

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db import models
from api.models import Application, Client, Resource
from api.widgets.file_upload import ClearableFileInputCustom
"""
{
  "application_id": "8c51224b-8a11-4ade-8066-2167d8d51dc9",
  "license_id": "8b090c89-f582-45f2-9fae-69698b25a288"
}"""

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'valid_until', 'application')
    readonly_fields = ('license',)

    def application(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_application_change", args=(obj.application.pk,)),
            obj.application.name
        ))

    def license(self, obj: Client):
        return mark_safe('<dd style="font-family: monospace;">{}</dd>'.format(
            obj.id
        ))

    application.short_description = 'Application'
    license.short_description = 'License'

class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'application')
    # Add it to the details view:
    readonly_fields = ('value_download',)
    formfield_overrides = {
        models.FileField: {'widget': ClearableFileInputCustom()},
    }

    def application(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_application_change", args=(obj.application.pk,)),
            obj.application.name
        ))

    def value_download(self, obj):
        if obj.data.name == '':
            return 'Empty'
        else:
            return mark_safe('<a href="data:application/octet-stream;base64,{0}" download="arquivo.txt">{1}</a>'.format(
            base64.b64encode(obj.data.read()).decode()
            , "Resource"))

    application.short_description = 'Application'
    value_download.short_description = 'Download'


# Register your models here.
admin.site.register(Application)
admin.site.register(Client, ClientAdmin)
admin.site.register(Resource, ResourceAdmin)
