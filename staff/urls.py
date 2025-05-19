from django.urls import path
from staff import views as staff_views
from .views import(TeacherDetailView,
                   TeacherUpdateView,TeacherDeleteView,
                   StaffDeleteView, StaffUpdateView, StaffDetailView)


app_name ='staff'

urlpatterns = [

     path('teacher_list/', staff_views.teachers_list, name='teacher-list'),
     path('staff_list/', staff_views.staff_list, name='staff-list'),
     path('assign_list/', staff_views.assign_list, name='assign-list'),

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