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
from attendance.models import AttendanceTotal, Attendance, AttendanceClass



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
    


@login_required()
def my_student(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    std_list = []
    for stud in ass.class_id.student_set.all():
        try:
            a = AttendanceTotal.objects.get(student=stud, subject=ass.subject)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, subject=ass.subject)
            a.save()
        std_list.append(a)
    # return render(request, 'staff/my_student_list.html', {'std_list': std_list})
    return render(request, 'staff/my_student_list.html', {'std_list': std_list, 'assign_id':assign_id})



@login_required
def my_clas(request, teacher_id, choice):
    teacher1 = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'attendance/t_clas.html', {'teacher1': teacher1, 'choice': choice})


