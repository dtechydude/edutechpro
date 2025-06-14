from django.contrib import admin
from .models import Hostel, Student, Badge
from import_export.admin import ImportExportModelAdmin



class HostelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name',]
    exclude = ('slug',)

class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       
    list_display=('user', 'first_name', 'standard','date_admitted', 'guardian_phone')
    list_filter = ['standard']
    search_fields = ('first_name', 'user__username')
    raw_id_fields = ['user', 'form_teacher', 'badge']


class BadgeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       
    list_display=('name',)
    exclude=('slug',)

# admin.site.register(StaffCategory)
admin.site.register(Hostel, HostelAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Badge, BadgeAdmin)


