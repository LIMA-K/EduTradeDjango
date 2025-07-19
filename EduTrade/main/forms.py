from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, TutorProfile

# Form for user login — we'll use Django's built-in AuthenticationForm in views

# Tutor User Registration Form (CustomUser)
class TutorRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        # TutorProfile Form (extra fields like phone, dept)
class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = ['phone_number', 'department']
