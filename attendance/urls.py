from django.urls import path
from . import views




app_name ='attendance'

urlpatterns = [
    path('student/<slug:stud_id>/attendance/', views.attendance, name='attendance'),
    path('student/<slug:stud_id>/<slug:subject_id>/attendance/', views.attendance_detail, name='attendance_detail'),


]