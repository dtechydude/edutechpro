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
from staff.models import Teacher, Staff


#Displays all teachers
def teachers_list(request):
    all_teachers = Teacher.objects.all().order_by('-date_employed')

    context ={
        'all_teachers':all_teachers
    }
    return render(request, 'staff/teachers_list.html', context)

#Displays all staff
def staff_list(request):
    all_staff = Staff.objects.all().order_by('-date_employed')

    context ={
        'all_staff':all_staff
    }
    return render(request, 'staff/staff_list.html', context)
