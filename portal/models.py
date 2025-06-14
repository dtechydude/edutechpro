from django.db import models
from django.db.models.signals import post_save, post_delete
from datetime import timedelta
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field
from embed_video.fields import EmbedVideoField
from django.core.exceptions import ValidationError
from djrichtextfield.models import RichTextField
# from staff.models import Teacher


# school departments e.g pre-nursery, nursery, junior sec, senior sec

class Dept(models.Model):
    id = models.CharField(primary_key='True', max_length=100)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# class Standard(models.Model):
#     # courses = models.ManyToManyField(Course, default=1)
#     id = models.CharField(primary_key='True', max_length=100)
#     dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
#     section = models.CharField(max_length=100)
#     sem = models.IntegerField()
#     teachers = models.ManyToManyField(Teacher, related_name='classrooms')

#     class Meta:
#         verbose_name_plural = 'classes'

#     def __str__(self):
#         d = Dept.objects.get(name=self.dept)
#         return '%s : %s %s' % (self.id, d.name, self.section)




# # Teacher Module
# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     id = models.CharField(primary_key=True, max_length=100)
#     full_name = models.CharField(max_length=100, help_text='First_Name, Middle_Name, Last_Name')
#     dept = models.ForeignKey(Dept, on_delete=models.CASCADE, default=1, related_name='my_dept')
#     class_in_charge = models.ForeignKey(Standard, on_delete=models.CASCADE, blank=True, null=True, related_name='myclasses')
    

#     female = 'female'
#     male = 'male'
#     select_gender = 'select_gender'
    
#     gender_type = [
#         ('female', female),
#         ('male', male),
#         ('select_gender', select_gender),
#     ]

#     gender= models.CharField(max_length=20, choices=gender_type, default= select_gender) 
#     DOB = models.DateField(default='1998-01-01')
#     date_employed = models.DateField(default='1998-01-01')

#     married = 'married'
#     single = 'single'
#     select = 'select'

#     marital_status = [
#         (married, 'married'),
#         (single, 'single'),
#         (select, 'select'),
#     ]

#     marital_status = models.CharField(max_length=15, choices=marital_status, default=select)
#     phone_home = models.CharField(max_length=15, null=True, blank=True)

#     # Academic information
#     qualification = models.CharField(max_length=150, default='OND')  
#     year = models.DateField(default='1998-01-01')   
#     institution = models.CharField(max_length=150, blank=True)
#     professional_body = models.CharField(max_length=150, blank=True)  
   
#     # Guarantor's information
#     guarantor_name = models.CharField(max_length=150, blank=True) 
#     guarantor_phone = models.CharField(max_length=15, blank=True) 
#     guarantor_address = models.CharField(max_length=150, blank=True) 
#     guarantor_email = models.CharField(max_length=60, blank=True)
    
#     # next of kin info
#     next_of_kin_name = models.CharField(max_length=60, blank=True)  
#     next_of_kin_address = models.CharField(max_length=150, blank=True)  
#     next_of_kin_phone = models.CharField(max_length=15, blank=True) 

#     form_teacher = 'form_teacher'
#     subject_teacher = 'subject_teacher'
#     principal = 'principal'
#     head_teacher = 'head_teacher'
  
    
#     staff_role = [
#         ('form_teacher', form_teacher),
#         ('subject_teacher', subject_teacher),
#         ('principal', principal),
#         ('head_teacher', head_teacher),
              
#     ]
#     staff_role= models.CharField(max_length=20, choices=staff_role, default=subject_teacher)
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#     active = models.BooleanField(default=False, blank=True)  

 
#     def __str__(self):
#         return self.full_name

