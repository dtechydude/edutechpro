# from django.db import models
# from django.db.models.signals import post_save, post_delete
# from datetime import timedelta
# from django.template.defaultfilters import slugify
# from django.contrib.auth.models import User
# from django.urls import reverse
# import os
# from django.utils.html import strip_tags
# from django_ckeditor_5.fields import CKEditor5Field
# from embed_video.fields import EmbedVideoField
# from django.core.exceptions import ValidationError
# from djrichtextfield.models import RichTextField
# # from portal.models import Teacher
# # from curriculum.models import Dept
# # from staff.models import Teacher


# class Dept(models.Model):
#     id = models.CharField(primary_key='True', max_length=100)
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

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
    

# # academic subjects
# class Subject(models.Model):
#     dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
#     id = models.CharField(primary_key='True', max_length=50)    
#     name = models.CharField(max_length=50)
#     shortname = models.CharField(max_length=50, default='X')
#     slug = models.SlugField(null=True, blank=True)

#     def __str__(self):
#         return self.name
    
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.name)
#         super().save(*args, **kwargs)

#     class Meta:
#       verbose_name = 'Subjects'
#       verbose_name_plural = 'Subjects'