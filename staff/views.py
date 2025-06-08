from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.db.models import Count
from django.db.models import F
#converting html to pdf
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from staff.models import Teacher, Staff, Assign
from students.models import Student
from curriculum.models import Class
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


# Specific to the login detail
class TeacherSelfDetailView(LoginRequiredMixin, DetailView):
    template_name = 'staff/teacher_self_detail.html'
    model = Teacher

    def get_object(self, queryset=None):
           if queryset is None:
               queryset = self.get_queryset()
           return queryset.filter(user=self.request.user).first()

# Specific to the login detail
class StaffSelfDetailView(LoginRequiredMixin, DetailView):
    template_name = 'staff/staff_self_detail.html'
    model = Staff

    def get_object(self, queryset=None):
           if queryset is None:
               queryset = self.get_queryset()
           return queryset.filter(user=self.request.user).first()



class TeacherDetailView(DetailView):
    template_name = 'staff/teacher_self_detail.html'
    context_object_name = 'teacher'
    queryset = Teacher.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Teacher, id=id_)


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


    
@login_required()
def my_student_in_class(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    std_list = []
    for stud in ass.class_id.student_set.all():       
        # std_list.append()
        return render(request, 'staff/my_own_students.html', {'std_list': std_list, 'assign_id':assign_id})

# students in a particular class
def student_in_a_class(request):
    # std_list = Student.objects.filter(class_id=F('USN'))
    # mystudent = PaymentDetail.objects.filter(student_id=User.objects.get(username=request.user))
    # mystudent = Student.objects.filter(class_id=Assign.objects.get(teacher_id=request.user))
    # mystudents = Assign.objects.filter(class_id=Student.objects.get())
    # class_in_charge = Assign.objects.get(teacher=request.user.teacher)
    # class_in_charges = Assign.objects.filter(class_id=Student.objects.get() )
    # class_in_charges = Student.objects.filter(class_id=Class.object.get(id=id))
    assign = Assign.objects.all()
    student = Student.objects.all()
    if assign.class_id == student.class_id:
        return render(request, 'staff/my_own_students.html', {'assign': assign, 'student':student})

def classroom_students(request, class_id):
    classroom = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(class_id=class_id)
    students_in_classroom = classroom.students.all().order_by('full_name')

    context = {
        'classroom': classroom,
        'students_in_classroom': students_in_classroom,
        'students':students
        
    }
    return render(request, 'staff/classroom_students.html', context)