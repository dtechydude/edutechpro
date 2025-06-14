from django.urls import path
from attendance import views as attendance_views






app_name ='attendance'

urlpatterns = [
    # path('', views.att_index, name='att_index'),
#     path('teacher/', views.index, name='index'),
#
# My Attendance Logic
    path('teacher/dashboard/', attendance_views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/attendance/<int:standard_id>/', attendance_views.mark_attendance, name='mark_attendance'),
    path('teacher/attendance/success/<int:standard_id>/', attendance_views.attendance_success, name='attendance_success'),

]

