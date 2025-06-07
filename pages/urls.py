
from django.urls import path
from pages import views as page_views
from . import views

app_name ='pages'

urlpatterns = [

     # path('', page_views.schoolly_home, name='schoolly-home'),
     path('', page_views.portal_home, name='portal-home'),
     path('help-center/', page_views.help_center, name='help-center'),
     path('lock-screen/', page_views.lock_screen, name='lock-screen'),

     path('<str:pk>/', views.StudentCardDetailView.as_view(), name='my_idcard'),

]
