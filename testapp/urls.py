# myapp/urls.py
from django.urls import path
from . import views


app_name ='testapp'
urlpatterns = [
    path('projects/<str:project_id>/tasks/create/', views.create_task, name='create_task'),
    path('projects/<str:project_id>/', views.project_detail, name='project_detail'),
    # ... other URL patterns
]