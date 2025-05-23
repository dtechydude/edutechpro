from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
   

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'user_type', 'phone', 'state_of_origin', ]



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [ 'email', 'last_name', 'first_name', ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'user_type', ]
        # widgets = {
        #     'date_of_birth': forms.DateInput(
        #         format=('%d/%m/%Y'),
        #         attrs={'class': 'form-control', 
        #                'placeholder': 'Select a date',
        #                'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
        #               }),
        # }




class UserTwoUpdateForm(forms.ModelForm):
   
    class Meta:
        model = User
        fields = [ 'last_name', ]


# class BusinessUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = [ '', ]

# class BankUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = [ 'bank_name', 'acc_no', 'acc_name', ]

# class KYCUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = [ 'date_of_birth', 'phone', 'nin', 'image', ]
#         widgets = {
#             'date_of_birth': forms.DateInput(
#                 format=('%d/%m/%Y'),
#                 attrs={'class': 'form-control', 
#                         'placeholder': 'Select a date',
#                         'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
#                         }),
#         }

# class RoleUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = [ 'user_role', ]
#         widgets = {
#             'date_of_birth': forms.DateInput(
#                 format=('%d/%m/%Y'),
#                 attrs={'class': 'form-control', 
#                         'placeholder': 'Select a date',
#                         'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
#                         }),
#         }
   
# class BioUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = [ 'gender', 'bio', ]

# # address update       
# class AddressUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = [ 'state', 'address', 'current_state' ]

# # Phone update       
# class PhoneUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = [ 'phone', 'altenate_phone' ]

# # Current State update       
# class CurrentStateUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = [ 'current_state',]
       
       
       