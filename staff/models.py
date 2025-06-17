from django.db import models
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from datetime import timedelta
from portal.models import Dept
# from curriculum.utils import Subject, Standard, Dept
from django.template.defaultfilters import slugify
# from portal.models import Standard, Dept



# Staff Module
class StaffPosition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=200, blank=True)
    slug = models.SlugField(null=True, blank=True, help_text='Do not enter anything here')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Staff Position'
        verbose_name_plural = 'Staff Position'

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20)   
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, default=1, related_name='my_depts')
    staff_position = models.ForeignKey(StaffPosition, on_delete=models.CASCADE, default=1)

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
    date_employed = models.DateField(default='1998-01-01')

    married = 'married'
    single = 'single'
    select = 'select'

    marital_status = [
        (married, 'married'),
        (single, 'single'),
        (select, 'select'),
    ]

    marital_status = models.CharField(max_length=15, choices=marital_status, default=select)
    phone_home = models.CharField(max_length=11, null=True, blank=True)

    # Academic information
    qualification = models.CharField(max_length=150, default='OND')  
    year = models.DateField(default='1998-01-01')   
    institution = models.CharField(max_length=150, blank=True)
    professional_body = models.CharField(max_length=150, blank=True)  
   
    # Guarantor's information
    guarantor_name = models.CharField(max_length=150, blank=True) 
    guarantor_phone = models.CharField(max_length=15, blank=True) 
    guarantor_address = models.CharField(max_length=150, blank=True) 
    guarantor_email = models.CharField(max_length=60, blank=True)
    
    # next of kin info
    next_of_kin_name = models.CharField(max_length=60, blank=True)  
    next_of_kin_address = models.CharField(max_length=150, blank=True)  
    next_of_kin_phone = models.CharField(max_length=15, blank=True) 

    form_teacher = 'form_teacher'
    subject_teacher = 'subject_teacher'
    principal = 'principal'
    head_teacher = 'head_teacher'
    admin_officer = 'admin_officer'
    account_officer = 'account_officer'
    non_academic = 'non_academic'
    others = 'others'
    select = 'select'

    
    staff_role = [
        ('form_teacher', form_teacher),
        ('subject_teacher', subject_teacher),
        ('principal', principal),
        ('head_teacher', head_teacher),
        ('admin_officer', admin_officer),
        ('account_officer', account_officer),
        ('non_academic', non_academic),
        ('others', others),
        ('select', select),
            
    ]
    staff_role= models.CharField(max_length=20, choices=staff_role, default=select)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

 
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Teacher Module
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20)   
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, default=1, related_name='my_dept')
    # class_in_charge = models.ForeignKey(Standard, on_delete=models.CASCADE, blank=True, null=True, related_name='myclasses')
    

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
    date_employed = models.DateField(default='1998-01-01')

    married = 'married'
    single = 'single'
    select = 'select'

    marital_status = [
        (married, 'married'),
        (single, 'single'),
        (select, 'select'),
    ]

    marital_status = models.CharField(max_length=15, choices=marital_status, default=select)
    phone_home = models.CharField(max_length=11, null=True, blank=True)

    # Academic information
    qualification = models.CharField(max_length=150, default='OND')  
    year = models.DateField(default='1998-01-01')   
    institution = models.CharField(max_length=150, blank=True)
    professional_body = models.CharField(max_length=150, blank=True)  
   
    # Guarantor's information
    guarantor_name = models.CharField(max_length=150, blank=True) 
    guarantor_phone = models.CharField(max_length=15, blank=True) 
    guarantor_address = models.CharField(max_length=150, blank=True) 
    guarantor_email = models.CharField(max_length=60, blank=True)
    
    # next of kin info
    next_of_kin_name = models.CharField(max_length=60, blank=True)  
    next_of_kin_address = models.CharField(max_length=150, blank=True)  
    next_of_kin_phone = models.CharField(max_length=15, blank=True) 

    form_teacher = 'form_teacher'
    subject_teacher = 'subject_teacher'
    principal = 'principal'
    head_teacher = 'head_teacher'
  
    
    staff_role = [
        ('form_teacher', form_teacher),
        ('subject_teacher', subject_teacher),
        ('principal', principal),
        ('head_teacher', head_teacher),
              
    ]
    staff_role= models.CharField(max_length=20, choices=staff_role, default=subject_teacher)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False, blank=True)  

 
    def __str__(self):
        return self.first_name
