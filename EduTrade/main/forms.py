from django import forms
from .models import CustomUser, TutorProfile, Course, Resource

# ------------------------------
# Tutor Registration Form
# ------------------------------
class TutorRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput, 
        required=False, 
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, 
        required=False, 
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean(self):
        """
        Validate that both passwords match if provided.
        Password is optional for existing users.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

# ------------------------------
# Tutor Profile Form
# ------------------------------
class TutorProfileForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = ['contact_info', 'phone_number', 'department']

# ------------------------------
# Course Form
# ------------------------------
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

# ------------------------------
# Resource Form
# ------------------------------
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['title', 'description', 'category', 'image', 'contact_info', 'exchange_type']
