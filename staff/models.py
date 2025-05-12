from django.db import models
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from datetime import timedelta
from curriculum.models import Class, Dept, Subject
from django.template.defaultfilters import slugify



time_slots = (
    ('7:30 - 8:30', '7:30 - 8:30'),
    ('8:30 - 9:30', '8:30 - 9:30'),
    ('9:30 - 10:30', '9:30 - 10:30'),
    ('11:00 - 11:50', '11:00 - 11:50'),
    ('11:50 - 12:40', '11:50 - 12:40'),
    ('12:40 - 1:30', '12:40 - 1:30'),
    ('2:30 - 3:30', '2:30 - 3:30'),
    ('3:30 - 4:30', '3:30 - 4:30'),
    ('4:30 - 5:30', '4:30 - 5:30'),
)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)


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
    id = models.CharField(primary_key=True, max_length=100)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, default=1)
    staff_position = models.ForeignKey(StaffPosition, on_delete=models.CASCADE, default=1)
    full_name = models.CharField(max_length=100, help_text='First_Name, Middle_Name, Last_Name')

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
    phone_home = models.CharField(max_length=15, null=True, blank=True)

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
        return self.full_name


# Teacher Module
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    id = models.CharField(primary_key=True, max_length=100)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, default=1)
    full_name = models.CharField(max_length=100, help_text='First_Name, Middle_Name, Last_Name')

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
    phone_home = models.CharField(max_length=15, null=True, blank=True)

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
        return self.full_name



class Assign(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('subject', 'class_id', 'teacher'),)

    def __str__(self):
        cl = Class.objects.get(id=self.class_id_id)
        cr = Subject.objects.get(id=self.subject_id)
        te = Teacher.objects.get(id=self.teacher_id)
        return '%s : %s : %s' % (te.full_name, cr.shortname, cl)
    

class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, choices=time_slots, default='11:00 - 11:50')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)
