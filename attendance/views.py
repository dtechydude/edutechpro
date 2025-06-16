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
from .utils import get_student_present_attendance_count # Import your utility function




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


# get attendance summary
def student_attendance_summary(request, USN):
    student = get_object_or_404(Student, USN=USN)

    # Define your date range (e.g., for the current month)
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = today.replace(day=28) # Start with 28, then adjust for month-end
    while last_day_of_month.month == today.month:
        try:
            last_day_of_month = last_day_of_month.replace(day=last_day_of_month.day + 1)
        except ValueError:
            break
    last_day_of_month = last_day_of_month.replace(day=last_day_of_month.day - 1)


    # You could also get dates from request.GET parameters if users specify a range
    # start_date_str = request.GET.get('start_date')
    # end_date_str = request.GET.get('end_date')
    # try:
    #     start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else first_day_of_month
    #     end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else last_day_of_month
    # except ValueError:
    #     # Handle invalid date format
    #     start_date = first_day_of_month
    #     end_date = last_day_of_month

    total_present_days = get_student_present_attendance_count(
        student_instance=student,
        start_date=first_day_of_month,
        end_date=last_day_of_month
    )

    context = {
        'student': student,
        'total_present_days': total_present_days,
        'start_date': first_day_of_month,
        'end_date': last_day_of_month,
    }
    return render(request, 'attendance/attendance_summary.html', context)


def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance/students_list.html', {'students':students})