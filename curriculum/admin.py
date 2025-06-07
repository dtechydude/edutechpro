from django.contrib import admin
from curriculum.models import SchoolIdentity
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import csv, datetime


class SchoolIdentityAdmin(admin.ModelAdmin):
           
    list_display=('name', 'phone1', 'email')
    exclude = ['slug',]
  


# Register your models here.
admin.site.register(SchoolIdentity, SchoolIdentityAdmin)