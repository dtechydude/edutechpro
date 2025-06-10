from django.urls import path
from staff import views as staff_views
from .views import(TeacherDetailView,
                   TeacherUpdateView,TeacherDeleteView,
                   StaffDeleteView, StaffUpdateView, StaffDetailView , StaffSelfDetailView, TeacherSelfDetailView)


app_name ='staff'

urlpatterns = [

     path('teacher_list/', staff_views.teachers_list, name='teacher-list'),
     path('staff_list/', staff_views.staff_list, name='staff-list'),
     path('assign_list/', staff_views.assign_list, name='assign-list'),
     path('my_teacher_view/', staff_views.my_teacher_view, name='my_teacher_view'),
     #students in my class
     path('my_student/', staff_views.student_in_a_class, name='my-students'),
    
    path('classroom/<str:class_id>/students/', staff_views.classroom_students, name='classroom_students'),

     path('staff-my-detail/', StaffSelfDetailView.as_view(), name="staff-self-detail"),
     path('teacher-my-detail/', TeacherSelfDetailView.as_view(), name="teacher-self-detail"),

     path('<str:id>/', TeacherDetailView.as_view(), name="teacher-detail"),
     path('<str:id>/update/', TeacherUpdateView.as_view(), name="teacher-update"),
     path('<str:id>/delete/', TeacherDeleteView.as_view(), name="teacher-delete"),

     path('<str:id>/', StaffDetailView.as_view(), name="staff-detail"),
     path('<str:id>/update/', StaffUpdateView.as_view(), name="staff-update"),
     path('<str:id>/delete/', StaffDeleteView.as_view(), name="staff-delete"),

     # Teacher's Own Student List
     path('teacher/<int:assign_id>/Students/attendance/', staff_views.my_student, name='my_student'),
     path('teacher/<slug:teacher_id>/<int:choice>/Classes/', staff_views.my_clas, name='my_clas'),


     

]