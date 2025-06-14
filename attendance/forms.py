from tkinter import Widget
from django import forms
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from attendance.models import Attendance




# My attendance Logic
class AttendanceForm(forms.ModelForm):
    # This form will be used for each student in the formset
    class Meta:
        model = Attendance
        fields = ['status'] # Only allow teacher to mark status
        widgets = {
            'status': forms.RadioSelect(choices=Attendance.STATUS_CHOICES),
        }

# This factory will create a form for each student
# We'll use this in the view
BaseAttendanceFormSet = modelformset_factory(
    Attendance,
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