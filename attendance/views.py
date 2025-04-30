from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import Dept, Class, Student, Attendance, Course, Teacher, Assign, AttendanceTotal, time_slots, \
    DAYS_OF_WEEK, AssignTime, AttendanceClass, StudentCourse, Marks, MarksClass

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from students.models import Student
from curriculum.models import Subject
from staff.models import Assign
from .models import AttendanceTotal, Attendance




# For Attendance View
@login_required()
def attendance(request, stud_id):
    stud = Student.objects.get(USN=stud_id)
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    att_list = []
    for ass in ass_list:
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'attendance/attendance.html', {'att_list': att_list})


@login_required()
def attendance_detail(request, stud_id, subject_id):
    stud = get_object_or_404(Student, USN=stud_id)
    cr = get_object_or_404(Subject, id=subject_id)
    att_list = Attendance.objects.filter(subject=cr, student=stud).order_by('date')
    return render(request, 'attendance/att_detail.html', {'att_list': att_list, 'cr': cr})