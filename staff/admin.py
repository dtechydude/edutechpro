from django.contrib import admin
from .models import Staff, StaffPosition



class StaffPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ['name',]

class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'dept')
    search_fields = ('full_name', 'dept__name')
    # ordering = ['dept__name', 'full_name']



# admin.site.register(StaffCategory)
admin.site.register(Staff, StaffAdmin)
admin.site.register(StaffPosition, StaffPositionAdmin)

