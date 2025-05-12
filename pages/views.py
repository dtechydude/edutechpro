from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth.models import User
from students.models import Student
from staff.models import Staff, Teacher, Assign
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def schoolly_home(request):
    return render(request, 'pages/homepage.html')

def portal_home(request):
    users_num = User.objects.count()
    student_num = Student.objects.count()
    num_student_inclass = Student.objects.filter().count()
    graduated = Student.objects.filter(student_status='graduated').count()
    dropped = Student.objects.filter(student_status='dropped').count()
    expelled = Student.objects.filter(student_status='expelled').count()
    suspended = Student.objects.filter(student_status='suspended').count()
    active = Student.objects.filter(student_status='active').count()
    staff_num = Teacher.objects.count()
    my_idcard = Student.objects.filter(user=User.objects.get(username=request.user))
    students = Student.objects.filter().order_by('class_id').values('class_id__section').annotate(count=Count('class_id__section'))
    my_students = Assign.objects.filter(teacher__user=request.user).order_by('class_id')
    no_inteacherclass = Assign.objects.filter(teacher__user=request.user).count()

    try:
        num_inclass = Student.objects.filter(class_id = request.user.student.class_id).count()
    except Student.DoesNotExist:
        num_inclass = Student.objects.filter()
    # Build a paginator with function based view
    queryset = Teacher.objects.all().order_by("-id")
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 40)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    
    context = {
        'student_num': student_num,
        'students' : students,
        'users_num': users_num,
        'num_inclass': num_inclass,
        'staff_num': staff_num,
        'graduated': graduated,
        'dropped': dropped,
        'expelled': expelled,
        'suspended': suspended,
        'active': active,
        'queryset': queryset,
        'events':events,
        'my_idcard':my_idcard,
        'my_students':my_students,
        'no_inteacherclass': no_inteacherclass
    }
    return render(request, 'pages/portal_home.html', context )
