from datetime import timedelta, datetime
from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import path

from .models import Student, Attendance,  Assign, AssignTime, AttendanceClass
from .models import  User, AttendanceRange
from curriculum.models import Class, Dept, Subject
from staff.models import Teacher, Assign, AssignTime
from students.models import StudentSubject, Marks

# Register your models here.

days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class ClassInline(admin.TabularInline):
    model = Class
    extra = 0


class DeptAdmin(admin.ModelAdmin):
    inlines = [ClassInline]
    list_display = ('name', 'id')
    search_fields = ('name', 'id')
    ordering = ['name']


class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    fk_name ='class_id'


class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'dept', 'sem', 'section')
    search_fields = ('id', 'dept__name', 'sem', 'section')
    ordering = ['dept__name', 'sem', 'section']
    inlines = [StudentInline]


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dept')
    search_fields = ('id', 'name', 'dept__name')
    ordering = ['dept', 'id']


class AssignTimeInline(admin.TabularInline):
    model = AssignTime
    extra = 0


class AssignAdmin(admin.ModelAdmin):
    inlines = [AssignTimeInline]
    list_display = ('class_id', 'subject', 'teacher')
    search_fields = ('class_id__dept__name', 'class_id__id', 'subject__name', 'teacher__name', 'subject__shortname')
    ordering = ['class_id__dept__name', 'class_id__id', 'subject__id']
    raw_id_fields = ['class_id', 'subject', 'teacher']


class MarksInline(admin.TabularInline):
    model = Marks
    extra = 0


class StudentSubjectAdmin(admin.ModelAdmin):
    inlines = [MarksInline]
    list_display = ('student', 'subject',)
    search_fields = ('student__name', 'subject__name', 'student__class_id__id', 'student__class_id__dept__name')
    ordering = ('student__class_id__dept__name', 'student__class_id__id', 'student__USN')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('USN', 'full_name', 'class_id', 'gender', 'student_status')
    search_fields = ('USN', 'full_name', 'class_id__id', 'class_id__dept__name')
    ordering = ['class_id__dept__name', 'class_id__id', 'USN']
    list_filter  = ['class_id__dept__name', 'gender', 'student_status']


# class TeacherAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'dept')
#     search_fields = ('full_name', 'dept__name')
#     ordering = ['dept__name', 'full_name']

    


class AttendanceClassAdmin(admin.ModelAdmin):
    list_display = ('assign', 'date', 'status')
    ordering = ['assign', 'date']
    change_list_template = 'admin/attendance/attendance_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('reset_attd/', self.reset_attd, name='reset_attd'),
        ]
        return my_urls + urls

    def reset_attd(self, request):

        start_date = datetime.strptime(request.POST['startdate'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['enddate'], '%Y-%m-%d').date()

        try:
            a = AttendanceRange.objects.all()[:1].get()
            a.start_date = start_date
            a.end_date = end_date
            a.save()
        except AttendanceRange.DoesNotExist:
            a = AttendanceRange(start_date=start_date, end_date=end_date)
            a.save()

        Attendance.objects.all().delete()
        AttendanceClass.objects.all().delete()
        for asst in AssignTime.objects.all():
            for single_date in daterange(start_date, end_date):
                if single_date.isoweekday() == days[asst.day]:
                    try:
                        AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=asst.assign)
                    except AttendanceClass.DoesNotExist:
                        a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign=asst.assign)
                        a.save()

        self.message_user(request, "Attendance Dates reset successfully!")
        return HttpResponseRedirect("../")


# admin.site.register(User, UserAdmin)
admin.site.register(Dept, DeptAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Subject, SubjectAdmin)
# admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Assign, AssignAdmin)
admin.site.register(StudentSubject, StudentSubjectAdmin)
admin.site.register(AttendanceClass, AttendanceClassAdmin)
