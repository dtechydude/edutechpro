from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


# from attendance.views import AttendanceAutocomplete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('pages.urls')),
    path('users/', include('users.urls', namespace='users')), 
    path('students/', include('students.urls', namespace='students')), 
    path('staff/', include('staff.urls', namespace='staff')), 
    path('payments/', include('payments.urls', namespace='payments')), 
    path('attendance/', include('attendance.urls', namespace='attendance')), 
    path('curriculum/', include('curriculum.urls', namespace='curriculum')),            

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)