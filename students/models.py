from django.db import models
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save, post_delete
from datetime import timedelta
from django.urls import reverse
from curriculum.models import Standard, Subject
from staff.models import Teacher
# from attendance.models import AttendanceTotal
from staff.models import Assign, AssignTime
from datetime import date




test_name = (
    ('Internal test 1', 'Internal test 1'),
    ('Internal test 2', 'Internal test 2'),
    ('Internal test 3', 'Internal test 3'),
    ('Event 1', 'Event 1'),
    ('Event 2', 'Event 2'),
    ('Semester End Exam', 'Semester End Exam'),
)

# Blood Group
A_Positive = 'A+'
A_Negative = 'A-'
B_Positive = 'B+'
AB_Positive = 'AB+'
AB_Negative = 'AB-'
O_Positive = 'O+'
O_Negative = 'O-'
select = 'select'


blood_group = [
    (A_Positive, 'A+'),
    (A_Negative, 'B-'),
    (B_Positive, 'B+'),
    (AB_Positive, 'AB+'),
    (AB_Negative, 'AB-'),
    (O_Positive, 'O+'),
    (O_Negative, 'O-'),
    (select, 'select'), 

]

# Genotype
AA = 'AA'
AS = 'AS'
AC = 'AC'
SS = 'SS'
select = 'select'

genotype = [
    (AA, 'AA'),
    (AS, 'AS'),
    (AC, 'AC'),
    (SS, 'SS'),
    (select, 'select'),
    
]


class Badge(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    desc = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__ (self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Hostel(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    desc = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(null=True, blank=True)
    
    def __str__ (self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, help_text='select user or add a new user')    
    USN = models.CharField(primary_key='True', max_length=100, help_text='Unique Student Number, Must be same as username')
    full_name = models.CharField(max_length=200, help_text='First_Name, Middle_name, Last_Name')
    class_id = models.ForeignKey(Standard, on_delete=models.CASCADE, default=1, related_name='students', help_text='The Student Current Class')
    class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True, related_name='teacher')
    badge =  models.ForeignKey(Badge, on_delete=models.CASCADE, blank=True, null=True, default='not a prefect', verbose_name='Prefect Tittle (if is prefect)')

    
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
    # medical information
    blood_group = models.CharField(max_length=15, choices=blood_group, default=select)
    genotype = models.CharField(max_length=15, choices=genotype, default=select)
    health_remark = models.CharField(max_length=60, blank=False, null=True, default='enter health detail')    

    day_student = 'day_student'
    boarder = 'boarder'

    student_types = [
        (day_student, 'day_student'),
        (boarder, 'boarder'),

    ]

    student_type = models.CharField(max_length=15, choices=student_types, default=day_student)
    hostel_name = models.ForeignKey(Hostel, on_delete=models.CASCADE, blank=True, null=True, related_name='hostel_name', verbose_name='hostel')
    date_admitted = models.DateField(default='2020-01-01')
    class_on_admission = models.ForeignKey(Standard, on_delete=models.CASCADE, blank=True, null=True, related_name='class_on_admission', verbose_name='class_on_admission')

     # Guardian details here..
    guardian_name = models.CharField(max_length=60, blank=False)  
    guardian_address = models.TextField(max_length=120, blank=True)  
    guardian_phone = models.CharField(max_length=15, blank=True)
    guardian_email = models.CharField(max_length=30, blank=True)

    select = 'select'
    parent = 'parent'
    father = 'father'   
    mother = 'mother'
    sister = 'sister'
    brother = 'brother'
    aunt = 'aunt'
    uncle = 'uncle'
    other = 'other'
    

    relationship = [
        (select, 'select'),
        (parent, 'parent'),
        (father, 'father'),
        (mother, 'mother'),
        (sister, 'sister'),
        (brother, 'brother'),
        (aunt, 'aunt'),
        (uncle, 'uncle'),
        (other, 'other'),          

    ]

    relationship = models.CharField(max_length=25, choices=relationship, default=select, help_text="Guardian's Relationship With Student")
    
    active = 'active'
    inactive = 'inactive'
    graduated = 'graduated'
    dropped = 'dropped'
    expelled = 'expelled'
    suspended = 'suspended'

    student_status = [
        (active, 'active'),
        (inactive, 'inactive'),
        (graduated, 'graduated'),
        (dropped, 'dropped'),
        (expelled, 'expelled'),
        (suspended, 'suspended'),

    ]

    student_status = models.CharField(max_length=15, choices=student_status, default=active)

    def __str__(self):
        return self.full_name
    
    class Meta:
        ordering = ['user']   
    
    def get_absolute_url(self):
        return reverse('students:student-detail', kwargs={'USN':self.USN})
    
# Student ID Card Generation
class StudentId(models.Model):
    id_card = models.BooleanField( default=False) 
    student = models.ForeignKey(Student, related_name='idcardimage', on_delete=models.CASCADE, blank=True, null=True, default=None,)
    f_1 = models.ImageField(default='school_id_header.jpg', upload_to='school_logo', help_text='Do not upload file')
    f_2 = models.ImageField(default='qr_code.jpg', upload_to='school_logo', help_text='Do not upload file')
    f_3 = models.ImageField(default='sign.jpg', upload_to='school_logo', help_text='Do not upload file')

    def __str__(self):
      return f"IdCard: {self.student}" 

    class Meta:
        verbose_name = 'Confirm to enable student generate ID Card'



#All subject offer by student
class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'subject'),)
        verbose_name_plural = 'Marks'

    def __str__(self):
        sname = Student.objects.get(full_name=self.student)
        cname = Subject.objects.get(name=self.subject)
        return '%s : %s' % (sname.full_name, cname.shortname)

    def get_cie(self):
        marks_list = self.marks_set.all()
        m = []
        for mk in marks_list:
            m.append(mk.marks1)
        cie = math.ceil(sum(m[:5]) / 2)
        return cie

    def get_attendance(self):
        a = AttendanceTotal.objects.get(student=self.student, course=self.subject)
        return a.attendance

class Marks(models.Model):
    studentcourse = models.ForeignKey(StudentSubject, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=test_name, default='Internal test 1')
    marks1 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        unique_together = (('studentcourse', 'name'),)

    @property
    def total_marks(self):
        if self.name == 'Semester End Exam':
            return 100
        return 20


class MarksClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=test_name, default='Internal test 1')
    status = models.BooleanField(default='False')

    class Meta:
        unique_together = (('assign', 'name'),)

    @property
    def total_marks(self):
        if self.name == 'Semester End Exam':
            return 100
        return 20
    



def create_marks(sender, instance, **kwargs):
    if kwargs['created']:
        if hasattr(instance, 'name'):
            ass_list = instance.class_id.assign_set.all()
            for ass in ass_list:
                try:
                    StudentSubject.objects.get(student=instance, subject=ass.subject)
                except StudentSubject.DoesNotExist:
                    sc = StudentSubject(student=instance, subject=ass.subject)
                    sc.save()
                    sc.marks_set.create(name='Internal test 1')
                    sc.marks_set.create(name='Internal test 2')
                    sc.marks_set.create(name='Internal test 3')
                    sc.marks_set.create(name='Event 1')
                    sc.marks_set.create(name='Event 2')
                    sc.marks_set.create(name='Semester End Exam')
        elif hasattr(instance, 'course'):
            stud_list = instance.class_id.student_set.all()
            cr = instance.subject
            for s in stud_list:
                try:
                    StudentSubject.objects.get(student=s, subject=cr)
                except StudentSubject.DoesNotExist:
                    sc = StudentSubject(student=s, subject=cr)
                    sc.save()
                    sc.marks_set.create(name='Internal test 1')
                    sc.marks_set.create(name='Internal test 2')
                    sc.marks_set.create(name='Internal test 3')
                    sc.marks_set.create(name='Event 1')
                    sc.marks_set.create(name='Event 2')
                    sc.marks_set.create(name='Semester End Exam')


def create_marks_class(sender, instance, **kwargs):
    if kwargs['created']:
        for name in test_name:
            try:
                MarksClass.objects.get(assign=instance, name=name[0])
            except MarksClass.DoesNotExist:
                m = MarksClass(assign=instance, name=name[0])
                m.save()


def delete_marks(sender, instance, **kwargs):
    stud_list = instance.class_id.student_set.all()
    StudentSubject.objects.filter(subject=instance.subject, student__in=stud_list).delete()


post_save.connect(create_marks, sender=Student)
post_save.connect(create_marks, sender=Assign)
post_save.connect(create_marks_class, sender=Assign)
# post_save.connect(create_attendance, sender=AssignTime)
post_delete.connect(delete_marks, sender=Assign)




#My Own Attendance

class Attendances(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=date.today)
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'), # Optional: if you want more granular status
        ('E', 'Excused'), # Optional
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    marked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    # Add any other relevant fields like remarks

    class Meta:
        unique_together = ('student', 'date') # A student can only have one attendance record per day

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.get_status_display()}"