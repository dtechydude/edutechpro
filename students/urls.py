from django.urls import path
from students import views as students_views


app_name ='students'

urlpatterns = [

     path('student_list/', students_views.student_list, name='student-list'),

     # Search student detail app
    path('student-search/', students_views.student_search_list, name='student_search_list'),
    path('search/', students_views.search, name='search'),
     

]