from django import forms
from payments.models import PaymentDetail, PaymentCategory, PaymentChart, BankDetail

# INLINE FORM STUFF
from django import forms
from django.forms.models import formset_factory



class PaymentCreateForm(forms.ModelForm):
        
        class Meta:
            model = PaymentDetail
            fields = '__all__'
            exclude = ('confirmed_a', 'confirmed_b', 'confirmed_c', 'discount', 'student_id', 'student_detail',)

            widgets = {
            'payment_date_a': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
        }
                        #Note that i removed user because it is an instance in the view already
                        

class PaymentForm(forms.ModelForm):
        
        class Meta:
            model = PaymentDetail
            fields = '__all__'
            exclude = ('confirmed', 'file',)

            widgets = {
            'payment_date': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
        }
                        #Note that i removed user because it is an instance in the view already



          
class PaymentCatForm(forms.ModelForm):
        
        class Meta:
            model = PaymentCategory
            fields = '__all__'
           

class BankRegisterForm(forms.ModelForm):
        
        class Meta:
            model = BankDetail
            fields = '__all__'


class PaymentUpdateForm(forms.ModelForm):
        
        class Meta:
            model = PaymentDetail
            fields = '__all__'
            exclude = ('confirmed', 'discount', 'file', 'student_id', 'student_detail',)

            widgets = {
            'payment_date_a' 'payment_date_b': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control', 
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                      }),
        }
                        #Note that i removed user because it is an instance in the view already



