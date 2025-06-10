from django.contrib import admin
from .models import Hostel
from import_export.admin import ImportExportModelAdmin



class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')
    search_fields = ('name',)
    ordering = ['name',]
    exclude = ('slug',)


# admin.site.register(StaffCategory)
admin.site.register(Hostel, HostelAdmin)


