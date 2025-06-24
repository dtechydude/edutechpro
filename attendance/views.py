# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponseRedirect
# from students.models import Student
# # from staff.models import Teacher, Assign
# from curriculum.models import Standard
# from attendance.models import Attendance
# from django.urls import reverse
# from django.utils import timezone
# from django.contrib.auth.decorators import login_required, user_passes_test
# from students.models import Student
# # from .models import AttendanceTotal, Attendance
# from attendance.forms import AttendanceFormSet, AttendanceForm
# from django.db import IntegrityError, transaction
# from datetime import date
# from .utils import get_student_present_attendance_count # Import your utility function




# # My Logic For Student Attendance
# # Helper function to check if the user is a teacher
# def is_teacher(user):
#     return hasattr(user, 'teacher') # Checks if the User object has an associated Teacher object

# @login_required
# @user_passes_test(is_teacher) # Ensures only teachers can access this view
# def mark_attendance(request, standard_id):
#     today = date.today()
#     teacher = request.user.teacher # Get the logged-in teacher object

#     classroom = get_object_or_404(Standard, id=standard_id)

#     # Ensure the logged-in teacher is assigned to this classroom
#     if teacher not in classroom.teachers.all():
#         return render(request, 'attendance/error_page.html', {'message': 'You are not assigned to this classroom.'})

#     students = classroom.students.all().order_by('last_name')

#     # Get existing attendance records for today for these students
#     initial_data = []
#     for student in students:
#         attendance_record, created = Attendance.objects.get_or_create(
#             student=student,
#             date=today,
#             defaults={'status': 'A', 'marked_by': teacher} # Default to absent if no record, marked by this teacher
#         )
#         initial_data.append({'id': attendance_record.id, 'status': attendance_record.status})

#     if request.method == 'POST':
#         formset = AttendanceFormSet(request.POST, queryset=Attendance.objects.filter(student__in=students, date=today))
#         if formset.is_valid():
#             instances = formset.save(commit=False) # Get the instances from the formset
#             try:
#                 with transaction.atomic():
#                     for instance in instances:
#                         instance.marked_by = teacher # Ensure the teacher is set
#                         instance.date = today # Ensure the date is today
#                         instance.save()
#                 return redirect('attendance:attendance_success', standard_id=classroom.id) # Redirect on success
#             except IntegrityError:
#                 # This should ideally not happen due to get_or_create, but good for robustness
#                 formset.add_error(None, "Could not save attendance due to a data conflict.")
#         else:
#             print(formset.errors) # Debugging formset errors
#     else:
#         # For GET request, populate formset with existing or default attendance
#         formset = AttendanceFormSet(queryset=Attendance.objects.filter(student__in=students, date=today))

#     context = {
#         'classroom': classroom,
#         'students': students,
#         'formset': formset,
#         'today': today,
#     }
#     return render(request, 'attendance/mark_attendance.html', context)

# @login_required
# @user_passes_test(is_teacher)
# def teacher_dashboard(request):
#     teacher = request.user.teacher    
#     assigned_classrooms = teacher.classrooms.all() # Get classrooms assigned to this teacher
#     context = {
#         'teacher': teacher,
#         'assigned_classrooms': assigned_classrooms,
#     }
#     return render(request, 'attendance/teacher_dashboard.html', context)

# @login_required
# @user_passes_test(is_teacher)
# def attendance_success(request, standard_id):
#     classroom = get_object_or_404(Standard, id=standard_id)
#     context = {
#         'classroom': classroom,
#     }
#     return render(request, 'attendance/attendance_success.html', context)


# def attendance_report(request):
#     attendance_report = Attendance.objects.all()
#     return render(request, 'attendance/attendance_report.html', {'attendance_report':attendance_report})


# # get attendance summary
# def student_attendance_summary(request, USN):
#     student = get_object_or_404(Student, USN=USN)

#     # Define your date range (e.g., for the current month)
#     today = date.today()
#     first_day_of_month = today.replace(day=1)
#     last_day_of_month = today.replace(day=28) # Start with 28, then adjust for month-end
#     while last_day_of_month.month == today.month:
#         try:
#             last_day_of_month = last_day_of_month.replace(day=last_day_of_month.day + 1)
#         except ValueError:
#             break
#     last_day_of_month = last_day_of_month.replace(day=last_day_of_month.day - 1)


#     # You could also get dates from request.GET parameters if users specify a range
#     # start_date_str = request.GET.get('start_date')
#     # end_date_str = request.GET.get('end_date')
#     # try:
#     #     start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else first_day_of_month
#     #     end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else last_day_of_month
#     # except ValueError:
#     #     # Handle invalid date format
#     #     start_date = first_day_of_month
#     #     end_date = last_day_of_month

#     total_present_days = get_student_present_attendance_count(
#         student_instance=student,
#         start_date=first_day_of_month,
#         end_date=last_day_of_month
#     )

#     context = {
#         'student': student,
#         'total_present_days': total_present_days,
#         'start_date': first_day_of_month,
#         'end_date': last_day_of_month,
#     }
#     return render(request, 'attendance/attendance_summary.html', context)


# def student_list(request):
#     students = Student.objects.all()
#     return render(request, 'attendance/students_list.html', {'students':students})




# from django.shortcuts import render, redirect, get_object_or_404
# from django.forms import modelformset_factory
# from django.contrib.auth.decorators import login_required
# from django.db import transaction
# from django.utils import timezone
# from staff.models import Teacher
# from students.models import Student
# from .models import Attendance
# from .forms import AttendanceForm



# THIS VIEW WORKS WELL WITH FIRST NAME
# @login_required
# def take_daily_attendance(request):
#     # Ensure the logged-in user is a teacher
#     try:
#         teacher = request.user.teacher
#     except Teacher.DoesNotExist:
#         return redirect('some_error_page_or_permission_denied') # Or handle appropriately

#     today = timezone.localdate()
#     students = Student.objects.filter(form_teacher=teacher).order_by('first_name')

#     # Prepare initial data for the formset
#     # We need to create an Attendance object for each student if one doesn't exist for today
#     # This ensures that all students appear in the formset, with their current attendance status
#     initial_data = []
#     for student in students:
#         attendance_record, created = Attendance.objects.get_or_create(
#             student=student,
#             date=today,
#             defaults={'present': False} # Default to absent if new
#         )
#         initial_data.append({
#             'id': attendance_record.id, # Crucial for updating existing records
#             'student': student.USN,
#             'present': attendance_record.present,
#             'student_name': student.first_name,# Pre-fill the read-only student name
#         })

#     # Create the ModelFormSet for Attendance
#     # queryset=Attendance.objects.none() means we are providing initial data, not querying directly
#     AttendanceFormSet = modelformset_factory(
#         Attendance,
#         form=AttendanceForm,
#         extra=0, # Do not add extra blank forms
#         can_delete=False # No need to delete attendance records this way
#     )

#     if request.method == 'POST':
#         formset = AttendanceFormSet(request.POST, queryset=Attendance.objects.filter(pk__in=[d['id'] for d in initial_data]))
#         # The queryset here ensures that the formset is trying to update
#         # only the specific Attendance instances we loaded or created.
#         # This is vital for managing existing records.

#         if formset.is_valid():
#             # Use a transaction to ensure all updates happen or none do
#             with transaction.atomic():
#                 # Loop through the forms in the formset
#                 for form in formset:
#                     if form.cleaned_data: # Check if the form has data (e.g., not deleted if can_delete was true)
#                         attendance_instance = form.save(commit=False) # Get instance without saving yet
#                         # The student and date are already set correctly by initial_data or get_or_create
#                         attendance_instance.save()
#             return redirect('attendance:attendance_success') # Redirect to a success page
#         else:
#             print(formset.errors) # Print formset errors to debug if issues persist
#             print(formset.non_form_errors()) # Print non-form errors too
#     else:
#         # For GET request, initialize the formset with the prepared data
#         formset = AttendanceFormSet(queryset=Attendance.objects.filter(pk__in=[d['id'] for d in initial_data]))
#         # Manually set initial for each form in the formset (ModelFormset does this automatically from queryset normally)
#         # but since we are providing pre-created records, it's good to ensure.
#         for i, form in enumerate(formset):
#             form.initial['student_name'] = initial_data[i]['student_name']

#     context = {
#         'formset': formset,
#         'today': today,
#         'teacher': teacher,
#     }
#     return render(request, 'attendance/take_attendance.html', context)




# # THIS VIEW WORKS WELL WITH THE FIRST AND LAST NAME
# from django.shortcuts import render, redirect, get_object_or_404
# from django.forms import modelformset_factory
# from django.contrib.auth.decorators import login_required
# from django.db import transaction
# from django.utils import timezone
# from .models import Attendance
# from .forms import AttendanceForm
# from students.models import Student
# from staff.models import Teacher

# @login_required
# def take_daily_attendance(request):
#     try:
#         teacher = request.user.teacher
#     except Teacher.DoesNotExist:
#         # Handle cases where the logged-in user is not associated with a Teacher profile
#         # Perhaps redirect to a login page, an error page, or show a message.
#         messages.error(request, "You are not authorized to view this page as a teacher.")
#         return redirect('some_other_page') # Define 'some_other_page' in your urls.py


#     today = timezone.localdate()
#     students = Student.objects.filter(form_teacher=teacher).order_by('first_name', 'last_name') # Order by names

#     initial_data = []
#     for student in students:
#         attendance_record, created = Attendance.objects.get_or_create(
#             student=student,
#             date=today,
#             defaults={'present': False}
#         )
#         initial_data.append({
#             'id': attendance_record.id,
#             'student': student.USN,
#             'present': attendance_record.present,
#             'student_full_name': student.get_full_name(), # Use the get_full_name method
#         })

#     AttendanceFormSet = modelformset_factory(
#         Attendance,
#         form=AttendanceForm,
#         extra=0,
#         can_delete=False
#     )

#     if request.method == 'POST':
#         formset = AttendanceFormSet(request.POST, queryset=Attendance.objects.filter(pk__in=[d['id'] for d in initial_data]))

#         if formset.is_valid():
#             with transaction.atomic():
#                 for form in formset:
#                     if form.cleaned_data:
#                         # form.save() will correctly update the existing attendance_instance
#                         # because 'id' is present in the form's fields and initial data.
#                         form.save()
#             return redirect('attendance:attendance_success')
#         else:
#             print(formset.errors)
#             print(formset.non_form_errors())
#     else:
#         # For GET request, initialize the formset with the prepared data
#         # Pass the queryset directly for ModelFormSet to pick up instances
#         # No need to manually iterate and set initial for student_full_name if initial_data is correctly structured
#         formset = AttendanceFormSet(queryset=Attendance.objects.filter(pk__in=[d['id'] for d in initial_data]))
#         # IMPORTANT: ModelFormSet usually handles initial data from the queryset.
#         # However, for our custom 'student_full_name' field, we need to manually set it for each form
#         # because it's not a direct model field.
#         for i, form in enumerate(formset):
#             form.initial['student_full_name'] = initial_data[i]['student_full_name']


#     context = {
#         'formset': formset,
#         'today': today,
#         'teacher': teacher,
#     }
#     return render(request, 'attendance/take_attendance.html', context)


# @login_required
# def attendance_success(request):
#     return render(request, 'attendance/attendance_success.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils import timezone
from django.contrib import messages # Import messages for error handling
from .models import Attendance
from students.models import Student
from staff.models import Teacher
from .forms import AttendanceDateForm, AttendanceForm, AttendanceReportForm # Import new forms

# Helper to get teacher profile, handles not found case
def get_teacher_profile(user):
    try:
        return user.teacher
    except Teacher.DoesNotExist:
        return None

@login_required
def take_daily_attendance(request):
    teacher = get_teacher_profile(request.user)
    if not teacher:
        messages.error(request, "You are not authorized to view this page as a teacher.")
        return redirect('/dashboard/') # Redirect to a safe page or login

    # Initialize the date form
    date_form = AttendanceDateForm(request.GET or None)
    selected_date = timezone.localdate() # Default to today
    if date_form.is_valid():
        selected_date = date_form.cleaned_data['date']

    students = Student.objects.filter(form_teacher=teacher).order_by('first_name', 'last_name')

    initial_data = []
    for student in students:
        attendance_record, created = Attendance.objects.get_or_create(
            student=student,
            date=selected_date, # Use the selected_date
            defaults={'present': False}
        )
        initial_data.append({
            'id': attendance_record.id,
            'student': student.USN,
            'present': attendance_record.present,
            'student_full_name': student.get_full_name(),
        })

    AttendanceFormSet = modelformset_factory(
        Attendance,
        form=AttendanceForm,
        extra=0,
        can_delete=False
    )

    if request.method == 'POST':
        # Re-initialize date_form for POST context if needed, though usually not directly used here
        date_form = AttendanceDateForm(request.POST) # Just for validation if needed, not to change selected date for formset
        formset = AttendanceFormSet(request.POST, queryset=Attendance.objects.filter(pk__in=[d['id'] for d in initial_data]))

        # We should also ensure the date form is valid if it's part of the submission
        # In this setup, date is passed via GET for initial load, and only POST for attendance
        # If date could be changed on POST, you'd add: `if date_form.is_valid() and formset.is_valid():`
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    if form.cleaned_data:
                        form.save()
            messages.success(request, f"Attendance for {selected_date.strftime('%Y-%m-%d')} saved successfully!")
            # Redirect to the same page with the selected date to show updated status
            return redirect('attendance:take_daily_attendance')
        else:
            messages.error(request, "There were errors saving attendance. Please check the form.")
            print(formset.errors)
            print(formset.non_form_errors())
    else:
        formset = AttendanceFormSet(queryset=Attendance.objects.filter(pk__in=[d['id'] for d in initial_data]))
        for i, form in enumerate(formset):
            form.initial['student_full_name'] = initial_data[i]['student_full_name']

    context = {
        'date_form': date_form, # Pass the date form to the template
        'formset': formset,
        'selected_date': selected_date, # Pass the selected date for display
        'teacher': teacher,
    }
    return render(request, 'attendance/take_attendance.html', context)

@login_required
def attendance_report(request):
    teacher = get_teacher_profile(request.user)
    if not teacher:
        messages.error(request, "You are not authorized to view this page as a teacher.")
        return redirect('/dashboard/')

    report_form = AttendanceReportForm(teacher=teacher, data=request.GET or None) # Pass teacher to form for queryset
    attendance_data = {} # Dictionary to hold structured report data

    if report_form.is_valid():
        student_filter = report_form.cleaned_data.get('student')
        start_date = report_form.cleaned_data.get('start_date')
        end_date = report_form.cleaned_data.get('end_date')

        # Build query for attendance records
        attendance_records_query = Attendance.objects.filter(
            student__form_teacher=teacher, # Filter by teacher's students
            date__range=[start_date, end_date]
        ).select_related('student').order_by('student__first_name', 'student__last_name', 'date')

        if student_filter:
            attendance_records_query = attendance_records_query.filter(student=student_filter)

        # Structure data for the template
        # Key: Student object, Value: Dictionary of {date: Attendance object}
        for record in attendance_records_query:
            if record.student not in attendance_data:
                attendance_data[record.student] = {}
            attendance_data[record.student][record.date] = record

    context = {
        'report_form': report_form,
        'attendance_data': attendance_data,
        'teacher': teacher,
    }
    return render(request, 'attendance/attendance_report.html', context)

# You can keep the attendance_success view or remove it and just use messages.success
# @login_required
# def attendance_success(request):
#     return render(request, 'myapp/attendance_success.html')
