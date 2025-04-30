from django.urls import path
from staff import views as staff_views


app_name ='staff'

urlpatterns = [

     path('teacher_list/', staff_views.teachers_list, name='teacher-list'),
     path('staff_list/', staff_views.staff_list, name='staff-list'),
     

]