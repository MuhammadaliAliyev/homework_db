from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *


class PatientSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')


class PatientChangeForm(UserChangeForm):
    phone_number = forms.CharField(max_length=15, required=False)
    email = forms.EmailField(required=False)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email', 'phone_number')


class DoctorSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15)
    specialization = forms.CharField(max_length=100)
    license_number = forms.CharField(max_length=50)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number',
                 'specialization', 'license_number')


class DoctorChangeForm(UserChangeForm):
    specialization = forms.CharField(max_length=100, required=False)
    license_number = forms.CharField(max_length=50, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    email = forms.EmailField(required=True)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email', 'phone_number', 'specialization', 'license_number')


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date_time', 'reason']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'prescription']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 4}),
            'prescription': forms.Textarea(attrs={'rows': 4}),
        }