# myapp/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_completed']
        # We intentionally omit 'project' here because we'll set it in the view