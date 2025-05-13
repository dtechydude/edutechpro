from django.urls import path
from students import views as students_views
from .views import StudentDetailView, StudentUpdateView, StudentDeleteView



app_name ='students'

urlpatterns = [

     path('student_list/', students_views.student_list, name='student-list'),
     
     path('<str:USN>/', StudentDetailView.as_view(), name="student-detail"),
     path('<str:USN>/update/', StudentUpdateView.as_view(), name="student-update"),
     path('<str:USN>/delete/', StudentDeleteView.as_view(), name="student-delete"), 

     # Search student detail app
    path('student-search/', students_views.student_search_list, name='student_search_list'),
    path('search/', students_views.search, name='search'),
     

    path('student/<slug:stud_id>/marks_list/', students_views.marks_list, name='marks_list'),


    path('teacher/<int:assign_id>/marks_list/', students_views.t_marks_list, name='t_marks_list'),
    path('teacher/<int:assign_id>/Students/Marks/', students_views.student_marks, name='t_student_marks'),
    path('teacher/<int:marks_c_id>/marks_entry/', students_views.t_marks_entry, name='t_marks_entry'),
    path('teacher/<int:marks_c_id>/marks_entry/confirm/', students_views.marks_confirm, name='marks_confirm'),
    path('teacher/<int:marks_c_id>/Edit_marks/', students_views.edit_marks, name='edit_marks'),
]