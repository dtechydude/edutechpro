from django.contrib import admin
from .models import Staff, StaffPosition, Teacher



class StaffPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ['name',]

class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'dept')
    search_fields = ('full_name', 'dept__name')
    # ordering = ['dept__name', 'full_name']
    
class TeacherAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'full_name', 'dept', 'staff_role' )
    search_fields = ('full_name', 'dept__name')
    ordering = ['dept__name', 'full_name']



# admin.site.register(StaffCategory)
admin.site.register(Staff, StaffAdmin)
admin.site.register(StaffPosition, StaffPositionAdmin)
admin.site.register(Teacher, TeacherAdmin)

