from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Count
#converting html to pdf
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from students.models import Student, StudentSubject
from staff.models import Assign
from students.forms import StudentUpdateForm
from users.forms import UserRegisterForm
# from curriculum.models import Standard
# from results.models import ResultSheet
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
import csv
# # for my rest_framework
# from .serializers import StudentDetailSerializer
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# For Filter
# from .filters import StudentFilter
# from django_filters.views import FilterView
# For panigation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template.loader import get_template
# from xhtml2pdf import pisa


#Displays all students
def student_list(request):
    all_students = Student.objects.all().order_by('-date_admitted')

    context ={
        'all_students':all_students
    }
    return render(request, 'students/student_list.html', context)


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

        results = Student.objects.filter(Q(full_name__icontains=query) | Q(student_type__icontains=query) | Q(class_id__dept__name__icontains=query) | Q(USN__icontains=query) | Q(guardian_name__icontains=query))

        
    return render(request, 'students/search.html', {'query': query, 'results': results})




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

        results = Student.objects.filter(Q(full_name__icontains=query) | Q(student_type__icontains=query) | Q(class_id__name__icontains=query) | Q(USN__icontains=query) | Q(guardian_name__icontains=query))

        
    return render(request, 'students/search.html', {'query': query, 'results': results})



class StudentDetailView(DetailView):
    template_name = 'students/student_detail.html'
    queryset = Student.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("USN")
        return get_object_or_404(Student, USN=id_)


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = StudentUpdateForm
    template_name = 'students/student_update_form.html'
    # queryset = StudentDetail.objects.all()


    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Student, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'students/student_delete.html'
    success_url = reverse_lazy('students:student-list')
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Student, id=id_)
    







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
