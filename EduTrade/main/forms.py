from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser, TutorProfile,Course

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

# Course Form
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'video_link', 'material']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'video_link': forms.URLInput(attrs={'class': 'form-control'}),
            'material': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
