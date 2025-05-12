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
from staff.models import Teacher, Staff, Assign
from staff.forms import TeacherUpdateForm, StaffRegisterForm, StaffUpdateForm



#Displays all teachers
def teachers_list(request):
    all_teachers = Teacher.objects.all().order_by('-date_employed')

    context = {
        'all_teachers': all_teachers
    }
    return render(request, 'staff/teachers_list.html', context)

#Displays all staff
def staff_list(request):
    all_staff = Staff.objects.all().order_by('-date_employed')

    context ={
        'all_staff': all_staff
    }
    return render(request, 'staff/staff_list.html', context)

def assign_list(request):
    assign = Assign.objects.all().order_by('-class_id')

    context ={
        'assign':assign
    }
    return render(request, 'staff/assign_list.html', context)


class TeacherDetailView(DetailView):
    template_name = 'staff/teacher_detail.html'
    queryset = Teacher.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("USN")
        return get_object_or_404(Teacher, USN=id_)


class TeacherUpdateView(LoginRequiredMixin, UpdateView):
    form_class = TeacherUpdateForm
    template_name = 'students/student_update_form.html'
    # queryset = StudentDetail.objects.all()


    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Teacher, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'staff/teacher_delete.html'
    success_url = reverse_lazy('staff:teacher-list')
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Teacher, id=id_)
    

# staff 
class StaffDetailView(DetailView):
    template_name = 'staff/staff_detail.html'
    queryset = Teacher.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("USN")
        return get_object_or_404(Staff, USN=id_)


class StaffUpdateView(LoginRequiredMixin, UpdateView):
    form_class = StaffUpdateForm
    template_name = 'students/staff_update_form.html'
    # queryset = StudentDetail.objects.all()


    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Staff, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

class StaffDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'staff/staff_delete.html'
    success_url = reverse_lazy('staff:staff-list')
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Staff, id=id_)