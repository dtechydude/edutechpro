from tkinter import Widget
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Attendances
from django.forms import modelformset_factory




class StudentRegisterForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'
        
        # widgets = {
        #     'date_employed': forms.DateInput(
        #         format=('%d/%m/%Y'),
        #         attrs={'class': 'form-control', 
        #                'placeholder': 'Select a date',
        #                'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
        #               }),

        #     'year': forms.DateInput(
        #         format=('%d/%m/%Y'),
        #         attrs={'class': 'form-control', 
        #                'placeholder': 'Select a date',
        #                'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
        #               }),

        #  }

       # Widget = {'date_employed': forms.DateInput()}

class StudentUpdateForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ('user',)



# My attendance Logic
class AttendanceForm(forms.ModelForm):
    # This form will be used for each student in the formset
    class Meta:
        model = Attendances
        fields = ['status'] # Only allow teacher to mark status
        widgets = {
            'status': forms.RadioSelect(choices=Attendances.STATUS_CHOICES),
        }

# This factory will create a form for each student
# We'll use this in the view
BaseAttendanceFormSet = modelformset_factory(
    Attendances,
    form=AttendanceForm,
    extra=0, # We'll dynamically set the number of forms based on students
    can_delete=False
)

# Custom formset to include student name for display
class AttendanceFormSet(BaseAttendanceFormSet):
    def __init__(self, *args, **kwargs):
        self.students = kwargs.pop('students', None)
        super().__init__(*args, **kwargs)
        if self.students:
            for i, form in enumerate(self.forms):
                # Attach student instance to each form for easy access in template
                form.instance.student = self.students[i]