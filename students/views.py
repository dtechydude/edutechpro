from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Count
#converting html to pdf
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from students.models import Student
from staff.models import Teacher
from students.forms import StudentUpdateForm
from users.forms import UserRegisterForm
from curriculum.models import SchoolIdentity
from curriculum.models import Standard
# from results.models import ResultSheet
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
import csv
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.db import IntegrityError, transaction
from datetime import date


#Displays all students
def student_list(request):
    all_students = Student.objects.all().order_by('-date_admitted')
    my_students = Student.objects.filter(class_teacher__user=request.user).order_by('user')

    
    context ={
        'all_students':all_students,
        'my_students':my_students
    }
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'students/student_list.html', context) 
    elif my_students:
        return render(request, 'students/my_student_list.html', context) 
    else:
         return render(request, 'pages/portal_home.html')
    
    
 # for boarding students   
def student_boarder_list(request):
    boarder_student = Student.objects.filter(student_type='boarder').order_by('-date_admitted')
    # boarder_student = Student.objects.all().order_by('-date_admitted')

    context ={
        'boarder_student':boarder_student
    }
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'students/student_boarder_list.html', context)
    else:
         return render(request, 'pages/portal_home.html')
    


# Student Search Query App
def student_search_list(request):
    student = Student.objects.all()
    
     # PAGINATOR METHOD
    page = request.GET.get('page', 1)
    paginator = Paginator(student, 30)
    try:
        student = paginator.page(page)
    except PageNotAnInteger:
        student = paginator.page(1)
    except EmptyPage:
        student = paginator.page(paginator.num_pages)

    return render(request, 'students/search_student_list.html', {'student': student })

# Define function to search student
def search(request):
    results = []

    if request.method == "GET":
        query = request.GET.get('search')

        if query == '':
            query = 'None'

        results = Student.objects.filter(Q(full_name__icontains=query) | Q(class_id__id__icontains=query) | Q(guardian_name__icontains=query) | Q(user__username__icontains=query) | Q(USN__icontains=query))
        # results = Student.objects.filter(Q(full_name__icontains=query))
        
    return render(request, 'students/search.html', {'query': query, 'results': results})

#count students in each class
def student_in_class(request):
    students = Student.objects.all()
    student_no = Student.objects.values('class_id').annotate(count=Count('class_id')).order_by('class_id')

    return render(request, 'students/student_no_in_class.html', {'students': students, 'student_no':student_no})


class StudentDetailView(DetailView):
    template_name = 'students/student_detail.html'
    queryset = Student.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("USN")
        return get_object_or_404(Student, USN=id_)
    
# Specific to the login detail
class StudentSelfDetailView(LoginRequiredMixin, DetailView):
    template_name = 'students/student_self_detail.html'
    model = Student

    def get_object(self, queryset=None):
           if queryset is None:
               queryset = self.get_queryset()
           return queryset.filter(user=self.request.user).first()


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = StudentUpdateForm
    template_name = 'students/student_update_form.html'
    # queryset = StudentDetail.objects.all()


    def get_object(self):
        id_ = self.kwargs.get("USN")
        return get_object_or_404(Student, USN=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'students/student_delete.html'
    success_url = reverse_lazy('students:student-list')
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Student, id=id_)
    



# Students Marks
@login_required()
def marks_list(request, stud_id):
    stud = Student.objects.get(USN=stud_id, )
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    sc_list = []
    for ass in ass_list:
        try:
            sc = StudentSubject.objects.get(student=stud, course=ass.course)
        except StudentSubject.DoesNotExist:
            sc = StudentSubject(student=stud, course=ass.course)
            sc.save()
            sc.marks_set.create(type='I', name='Internal test 1')
            sc.marks_set.create(type='I', name='Internal test 2')
            sc.marks_set.create(type='I', name='Internal test 3')
            sc.marks_set.create(type='E', name='Event 1')
            sc.marks_set.create(type='E', name='Event 2')
            sc.marks_set.create(type='S', name='Semester End Exam')
        sc_list.append(sc)

    return render(request, 'students/marks_list.html', {'sc_list': sc_list})


# teacher marks

@login_required()
def t_marks_list(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    m_list = MarksClass.objects.filter(assign=ass)
    return render(request, 'students/t_marks_list.html', {'m_list': m_list})


@login_required()
def t_marks_entry(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    ass = mc.assign
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
        'mc': mc,
    }
    return render(request, 'students/t_marks_entry.html', context)


@login_required()
def marks_confirm(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    ass = mc.assign
    cr = ass.subject
    cl = ass.class_id
    for s in cl.student_set.all():
        mark = request.POST[s.USN]
        sc = StudentSubject.objects.get(subject=cr, student=s)
        m = sc.marks_set.get(name=mc.name)
        m.marks1 = mark
        m.save()
    mc.status = True
    mc.save()

    return HttpResponseRedirect(reverse('students:t_marks_list', args=(ass.id,)))


@login_required()
def edit_marks(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    cr = mc.assign.subject
    stud_list = mc.assign.class_id.student_set.all()
    m_list = []
    for stud in stud_list:
        sc = StudentSubject.objects.get(subject=cr, student=stud)
        m = sc.marks_set.get(name=mc.name)
        m_list.append(m)
    context = {
        'mc': mc,
        'm_list': m_list,
    }
    return render(request, 'students/edit_marks.html', context)


@login_required()
def student_marks(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    sc_list = StudentSubject.objects.filter(student__in=ass.class_id.student_set.all(), subject=ass.subject)
    return render(request, 'students/t_student_marks.html', {'sc_list': sc_list})



#generate IDCARD PDF
@login_required
def id_render_pdf_view(request, *args, **kwargs):    

    pk = kwargs.get('pk')
    
    student_detail = get_object_or_404(Student, pk=pk)
    school_identity = SchoolIdentity.objects.get()
    template_path = 'students/student_id_pdf.html'
    # template_path = 'results/result_sheet.html'
    context = {'student_detail': student_detail, 'school_identity':school_identity }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if you want to download
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if you just want to display
    response['Content-Disposition'] = 'filename="id_card.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
    html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


class MyTeacherDetailView(DetailView):
    template_name = 'student/my_teacher_detail.html'
    context_object_name = 'teacher'
    queryset = Teacher.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Teacher, id=id_)
    
def my_class_teacher(request):
    student = Student.objects.filter(user = request.user)
    my_teacher = Teacher.objects.get(class_in_charge=student.class_id)
    return render (request, 'students/my_teacher_detail.html', {'my_teacher':my_teacher})

