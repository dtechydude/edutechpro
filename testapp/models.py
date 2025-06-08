# myapp/models.py
from django.db import models
from django.contrib.auth.models import User # Django's built-in User model
from django.urls import reverse

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # Foreign key to the User model, indicating who owns this project
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('testapp:project_detail', kwargs={'id':self.id})

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Foreign key to the Project model
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    