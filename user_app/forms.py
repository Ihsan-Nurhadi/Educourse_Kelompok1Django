from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    profile_pic = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control-file"
            }
        ),
        required=False  # Optional profile picture
    )
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(
            attrs={
                "class": "form-check-input"
            }
        ),
        required=True  # At least one role must be selected
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'profile_pic')

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data['role']
        
        # Set the role based on the selected choice
        if role == 'teacher':
            user.is_teacher = True
            user.is_student = False
        else:
            user.is_teacher = False
            user.is_student = True
        
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic']