from django.db import models
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from datetime import timedelta
from curriculum.models import Subject
from students.models import Student
from staff.models import Teacher
from datetime import date



#My Own Attendance

class Attendance(models.Model):
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
        return f"{self.student.first_name}  {self.student.last_name} - {self.date} - {self.get_status_display()}"