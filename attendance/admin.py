from datetime import timedelta, datetime
from django.contrib import admin
from .models import Attendance
# # from django.contrib.auth.admin import UserAdmin
# from django.http import HttpResponseRedirect
# from django.urls import path
# from import_export.admin import ImportExportModelAdmin
# from .models import Student, Attendance,  Assign, AssignTime, AttendanceClass
# from .models import  User, AttendanceRange
# from curriculum.models import Subject, Session, Standard, Dept
# from staff.models import Teacher, Assign, AssignTime
# from students.models import StudentSubject, Marks, StudentId
# # from portal.models import Standard, Dept

# # Register your models here.


class AttendanceAdmin(admin.ModelAdmin):
 
    list_display = ('student', 'date',  'status', 'marked_by' )
  

admin.site.register(Attendance, AttendanceAdmin)
