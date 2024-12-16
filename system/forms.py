from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Company, WorkerProfile

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

class ManagerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'company']

class WorkerRegistrationForm(forms.ModelForm):
    class Meta:
        model = WorkerProfile
        fields = ['first_name', 'last_name', 'salary', 'phone_number', 'position']

class WorkerUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
