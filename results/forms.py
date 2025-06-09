from django import forms
from results.models import MarkedSheet, UploadCertificate, ResultSheet1, ResultSheet2
#from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


class ResultUploadForm(forms.ModelForm):
        
        class Meta:
            model = MarkedSheet
            fields = '__all__'

            widgets = {
            'exam_date': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
        }

           

class PrintCertificateForm(forms.ModelForm):
        
        class Meta:
            model = UploadCertificate
            fields =  '__all__'

            widgets = {
            'exam_year': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
        }


class ResultCreateForm(forms.ModelForm):
        
        class Meta:
            model = ResultSheet1
            fields =  '__all__'
            exclude = ('student_id',)

            widgets = {
            'exam_date' : forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),

             'next_term_resume' : forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
        }

       

class ResultUpdateForm(forms.ModelForm):
    class Meta:
        model = ResultSheet1
        fields = '__all__'
        exclude = ('student_id', 'publish', 'remark', 'class_teacher_comment', 'principal_comment', 'next_term_resume')
        # exclude = ('user',)

class ResultUpdateForm2(forms.ModelForm):
    class Meta:
        model = ResultSheet2
        fields = '__all__'
        exclude = ('student_id', 'publish', 'remark', 'class_teacher_comment', 'principal_comment', 'next_term_resume')
        # exclude = ('user',)
       