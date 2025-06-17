from django.contrib import admin
from .models import Staff, StaffPosition, Teacher
from import_export.admin import ImportExportModelAdmin



class StaffPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ['name',]
    exclude = ('slug',)

class StaffAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('first_name', 'dept', 'phone_home', 'qualification', 'date_employed')
    search_fields = ('first_name', 'dept__name')
    # ordering = ['dept__name', 'full_name']
    
class TeacherAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ( 'user', 'first_name', 'dept', 'staff_role', 'phone_home' )
    search_fields = ('first_name', 'dept__name')
    ordering = ['dept__name', 'first_name']



# admin.site.register(StaffCategory)
admin.site.register(Staff, StaffAdmin)
admin.site.register(StaffPosition, StaffPositionAdmin)
admin.site.register(Teacher, TeacherAdmin)

