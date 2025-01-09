from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Patient



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class PatientProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['image','bio','gender','height','weight','location','phone_number','activity_level','dob','bmi','bmr']

    bmi = forms.FloatField(required=False)
    bmr = forms.FloatField(required=False)

