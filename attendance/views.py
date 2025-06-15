from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from students.models import Student
# from staff.models import Teacher, Assign
from curriculum.models import Standard
from attendance.models import Attendance
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from students.models import Student
# from .models import AttendanceTotal, Attendance
from attendance.forms import AttendanceFormSet, AttendanceForm
from django.db import IntegrityError, transaction
from datetime import date




# # @login_required
# # def att_index(request):
# #     if request.user.teacher:
# #         return render(request, 'attendance/t_homepage.html')
# #     if request.user.student:
# #         return render(request, 'attendance/homepage.html')
# #     return render(request, 'info/logout.html')

# @login_required
# def index(request):
#     if request.user.teacher:
#         return render(request, 'attendance/t_homepage.html')
#     # if request.user.studentdetail.student_status == 'active':
#     #     return render(request, 'attendance/homepage.html')
#     # return render(request, 'attendance/logout.html'


# # For Attendance View
# @login_required()
# def attendance(request, stud_id):
#     stud = Student.objects.get(USN=stud_id)
#     ass_list = Assign.objects.filter(class_id_id=stud.class_id)
#     att_list = []
#     for ass in ass_list:
#         try:
#             a = AttendanceTotal.objects.get(student=stud, subject=ass.subject)
#         except AttendanceTotal.DoesNotExist:
#             a = AttendanceTotal(student=stud, subject=ass.subject)
#             a.save()
#         att_list.append(a)
#     return render(request, 'attendance/attendance.html', {'att_list': att_list})


# @login_required()
# def attendance_detail(request, stud_id, subject_id):
#     stud = get_object_or_404(Student, USN=stud_id)
#     cr = get_object_or_404(Subject, id=subject_id)
#     att_list = Attendance.objects.filter(subject=cr, student=stud).order_by('date')
#     return render(request, 'attendance/att_detail.html', {'att_list': att_list, 'cr': cr})



# # Teacher Views

# @login_required
# def t_clas(request, teacher_id, choice):
#     teacher1 = get_object_or_404(Teacher, id=teacher_id)
#     return render(request, 'attendance/t_clas.html', {'teacher1': teacher1, 'choice': choice})


# @login_required()
# def t_student(request, assign_id):
#     ass = Assign.objects.get(id=assign_id)
#     att_list = []
#     for stud in ass.class_id.student_set.all():
#         try:
#             a = AttendanceTotal.objects.get(student=stud, subject=ass.subject)
#         except AttendanceTotal.DoesNotExist:
#             a = AttendanceTotal(student=stud, subject=ass.subject)
#             a.save()
#         att_list.append(a)
#     return render(request, 'attendance/t_students.html', {'att_list': att_list})


# @login_required()
# def t_class_date(request, assign_id):
#     now = timezone.now()
#     ass = get_object_or_404(Assign, id=assign_id)
#     att_list = ass.attendanceclass_set.filter(date__lte=now).order_by('-date')
#     return render(request, 'attendance/t_class_date.html', {'att_list': att_list})


# @login_required()
# def cancel_class(request, ass_c_id):
#     assc = get_object_or_404(AttendanceClass, id=ass_c_id)
#     assc.status = 2
#     assc.save()
#     return HttpResponseRedirect(reverse('t_class_date', args=(assc.assign_id,)))


# @login_required()
# def t_attendance(request, ass_c_id):
#     assc = get_object_or_404(AttendanceClass, id=ass_c_id)
#     ass = assc.assign
#     c = ass.class_id
#     context = {
#         'ass': ass,
#         'c': c,
#         'assc': assc,
#     }
#     return render(request, 'attendance/t_attendance.html', context)


# @login_required()
# def edit_att(request, ass_c_id):
#     assc = get_object_or_404(AttendanceClass, id=ass_c_id)
#     cr = assc.assign.subject
#     att_list = Attendance.objects.filter(attendanceclass=assc, subject=cr)
#     context = {
#         'assc': assc,
#         'att_list': att_list,
#     }
#     return render(request, 'attendance/t_edit_att.html', context)


# @login_required()
# def confirm(request, ass_c_id):
#     assc = get_object_or_404(AttendanceClass, id=ass_c_id)
#     ass = assc.assign
#     cr = ass.subject
#     cl = ass.class_id
#     for i, s in enumerate(cl.student_set.all()):
#         status = request.POST[s.USN]
#         if status == 'present':
#             status = 'True'
#         else:
#             status = 'False'
#         if assc.status == 1:
#             try:
#                 a = Attendance.objects.get(subject=cr, student=s, date=assc.date, attendanceclass=assc)
#                 a.status = status
#                 a.save()
#             except Attendance.DoesNotExist:
#                 a = Attendance(subject=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
#                 a.save()
#         else:
#             a = Attendance(subject=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
#             a.save()
#             assc.status = 1
#             assc.save()

#     return HttpResponseRedirect(reverse('attendance:t_class_date', args=(ass.id,)))


# @login_required()
# def t_attendance_detail(request, stud_id, subject_id):
#     stud = get_object_or_404(Student, USN=stud_id)
#     cr = get_object_or_404(Subject, id=subject_id)
#     att_list = Attendance.objects.filter(subject=cr, student=stud).order_by('date')
#     return render(request, 'attendance/t_att_detail.html', {'att_list': att_list, 'cr': cr})


# @login_required()
# def change_att(request, att_id):
#     a = get_object_or_404(Attendance, id=att_id)
#     a.status = not a.status
#     a.save()
#     return HttpResponseRedirect(reverse('attendance:t_attendance_detail', args=(a.student.USN, a.subject_id)))


# @login_required()
# def t_extra_class(request, assign_id):
#     ass = get_object_or_404(Assign, id=assign_id)
#     c = ass.class_id
#     context = {
#         'ass': ass,
#         'c': c,
#     }
#     return render(request, 'attendance/t_extra_class.html', context)


# @login_required()
# def e_confirm(request, assign_id):
#     ass = get_object_or_404(Assign, id=assign_id)
#     cr = ass.subject
#     cl = ass.class_id
#     assc = ass.attendanceclass_set.create(status=1, date=request.POST['date'])
#     assc.save()

#     for i, s in enumerate(cl.student_set.all()):
#         status = request.POST[s.USN]
#         if status == 'present':
#             status = 'True'
#         else:
#             status = 'False'
#         date = request.POST['date']
#         a = Attendance(subject=cr, student=s, status=status, date=date, attendanceclass=assc)
#         a.save()

#     return HttpResponseRedirect(reverse('attendance:t_clas', args=(ass.teacher_id, 1)))



# @login_required()
# def t_report(request, assign_id):
#     ass = get_object_or_404(Assign, id=assign_id)
#     sc_list = []
#     for stud in ass.class_id.student_set.all():
#         a = StudentSubject.objects.get(student=stud, subject=ass.subject)
#         sc_list.append(a)
#     return render(request, 'attendance/t_report.html', {'sc_list': sc_list})


# @login_required()
# def timetable(request, class_id):
#     asst = AssignTime.objects.filter(assign__class_id=class_id)
#     matrix = [['' for i in range(12)] for j in range(6)]

#     for i, d in enumerate(DAYS_OF_WEEK):
#         t = 0
#         for j in range(12):
#             if j == 0:
#                 matrix[i][0] = d[0]
#                 continue
#             if j == 4 or j == 8:
#                 continue
#             try:
#                 a = asst.get(period=time_slots[t][0], day=d[0])
#                 matrix[i][j] = a.assign.subject_id
#             except AssignTime.DoesNotExist:
#                 pass
#             t += 1

#     context = {'matrix': matrix}
#     return render(request, 'attendance/timetable.html', context)


# @login_required()
# def t_timetable(request, teacher_id):
#     asst = AssignTime.objects.filter(assign__teacher_id=teacher_id)
#     class_matrix = [[True for i in range(12)] for j in range(6)]
#     for i, d in enumerate(DAYS_OF_WEEK):
#         t = 0
#         for j in range(12):
#             if j == 0:
#                 class_matrix[i][0] = d[0]
#                 continue
#             if j == 4 or j == 8:
#                 continue
#             try:
#                 a = asst.get(period=time_slots[t][0], day=d[0])
#                 class_matrix[i][j] = a
#             except AssignTime.DoesNotExist:
#                 pass
#             t += 1

#     context = {
#         'class_matrix': class_matrix,
#     }
#     return render(request, 'attendance/t_timetable.html', context)


# @login_required()
# def free_teachers(request, asst_id):
#     asst = get_object_or_404(AssignTime, id=asst_id)
#     ft_list = []
#     t_list = Teacher.objects.filter(assign__class_id__id=asst.assign.class_id_id)
#     for t in t_list:
#         at_list = AssignTime.objects.filter(assign__teacher=t)
#         if not any([True if at.period == asst.period and at.day == asst.day else False for at in at_list]):
#             ft_list.append(t)

#     return render(request, 'attendance/free_teachers.html', {'ft_list': ft_list})




# My Logic For Student Attendance
# Helper function to check if the user is a teacher
def is_teacher(user):
    return hasattr(user, 'teacher') # Checks if the User object has an associated Teacher object

@login_required
@user_passes_test(is_teacher) # Ensures only teachers can access this view
def mark_attendance(request, standard_id):
    today = date.today()
    teacher = request.user.teacher # Get the logged-in teacher object

    classroom = get_object_or_404(Standard, id=standard_id)

    # Ensure the logged-in teacher is assigned to this classroom
    if teacher not in classroom.teachers.all():
        return render(request, 'attendance/error_page.html', {'message': 'You are not assigned to this classroom.'})

    students = classroom.students.all().order_by('last_name')

    # Get existing attendance records for today for these students
    initial_data = []
    for student in students:
        attendance_record, created = Attendance.objects.get_or_create(
            student=student,
            date=today,
            defaults={'status': 'A', 'marked_by': teacher} # Default to absent if no record, marked by this teacher
        )
        initial_data.append({'id': attendance_record.id, 'status': attendance_record.status})

    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST, queryset=Attendance.objects.filter(student__in=students, date=today))
        if formset.is_valid():
            instances = formset.save(commit=False) # Get the instances from the formset
            try:
                with transaction.atomic():
                    for instance in instances:
                        instance.marked_by = teacher # Ensure the teacher is set
                        instance.date = today # Ensure the date is today
                        instance.save()
                return redirect('attendance:attendance_success', standard_id=classroom.id) # Redirect on success
            except IntegrityError:
                # This should ideally not happen due to get_or_create, but good for robustness
                formset.add_error(None, "Could not save attendance due to a data conflict.")
        else:
            print(formset.errors) # Debugging formset errors
    else:
        # For GET request, populate formset with existing or default attendance
        formset = AttendanceFormSet(queryset=Attendance.objects.filter(student__in=students, date=today))

    context = {
        'classroom': classroom,
        'students': students,
        'formset': formset,
        'today': today,
    }
    return render(request, 'attendance/mark_attendance.html', context)

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = request.user.teacher    
    assigned_classrooms = teacher.classrooms.all() # Get classrooms assigned to this teacher
    context = {
        'teacher': teacher,
        'assigned_classrooms': assigned_classrooms,
    }
    return render(request, 'attendance/teacher_dashboard.html', context)

@login_required
@user_passes_test(is_teacher)
def attendance_success(request, standard_id):
    classroom = get_object_or_404(Standard, id=standard_id)
    context = {
        'classroom': classroom,
    }
    return render(request, 'attendance/attendance_success.html', context)


def attendance_report(request):
    attendance_report = Attendance.objects.all()
    return render(request, 'attendance/attendance_report.html', {'attendance_report':attendance_report})