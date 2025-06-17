from datetime import timedelta, datetime
from django.contrib import admin
from .models import Attendance


class AttendanceAdmin(admin.ModelAdmin):
 
    list_display = ('student', 'date',  'status', 'marked_by' )
  

admin.site.register(Attendance, AttendanceAdmin)
