
from django.urls import path
from pages import views as page_views

app_name ='pages'

urlpatterns = [

     # path('', page_views.schoolly_home, name='schoolly-home'),
     path('', page_views.portal_home, name='portal-home'),

]
