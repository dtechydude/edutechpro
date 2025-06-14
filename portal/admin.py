from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from portal.models import Dept

# Register your models here.

class DeptAdmin(admin.ModelAdmin):
       
    list_display=('name',)
    list_filter  = ['name',]
    search_fields = ('name',)
    # raw_id_fields = ['name',]


admin.site.register(Dept, DeptAdmin)
