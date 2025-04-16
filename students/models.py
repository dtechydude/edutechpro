from django.db import models
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from datetime import timedelta
from curriculum.models import Class



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)    
    USN = models.CharField(primary_key='True', max_length=100, help_text='Unique Student Number')
    middle_name = models.CharField(max_length=200)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, default=1)
    
    female = 'female'
    male = 'male'
    select_gender = 'select_gender'
    
    gender_type = [
        ('female', female),
        ('male', male),
        ('select_gender', select_gender),
    ]

    gender= models.CharField(max_length=20, choices=gender_type, default= select_gender) 
    DOB = models.DateField(default='1998-01-01')

    def __str__(self):
        return self.middle_name