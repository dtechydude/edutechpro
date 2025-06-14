from django.contrib import admin
from .models import Hostel, Student, Badge
from import_export.admin import ImportExportModelAdmin



class HostelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ['name',]
    exclude = ('slug',)

class StudentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       
    list_display=('USN', 'full_name', 'class_id','date_admitted', 'guardian_phone')
    list_filter = ['class_id']
    search_fields = ('full_name', 'user__username')
    raw_id_fields = ['user', 'class_teacher', 'badge']


class BadgeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
       
    list_display=('name',)
    exclude=('slug',)

# admin.site.register(StaffCategory)
admin.site.register(Hostel, HostelAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Badge, BadgeAdmin)


