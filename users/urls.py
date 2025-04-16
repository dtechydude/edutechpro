from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views 
from django.contrib.auth import views as auth_views


app_name ='users'

urlpatterns = [
    path('register/', user_views.register, name="register"),
    path('student-staff/', user_views.student_staff, name="student_staff"),
    # path('login/', user_views.user_login, name="login"),
    path('dashboard/', user_views.users_home, name="users_home"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('profile/', user_views.profile, name="profile"),
    path('logout/', user_views.user_logout, name='user_logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    
   
]
