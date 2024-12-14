from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Contact, IklanPromosi

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

class ContactForm(forms.ModelForm):
    firstName = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control",'placeholder': 'First Name'
            }
        )
    )
    lastName = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control", 'placeholder': 'Last Name'
            }
        )
    )
    email = forms.CharField(
        widget= forms.EmailInput(
            attrs={
                "class": "form-control", 'placeholder': 'Email@gmail.com'
            }
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control", 'placeholder': 'Your Message'
            }
        )
    )

    class Meta:
        model = Contact
        fields = ['firstName', 'lastName', 'email', 'message']

    def save(self, commit=True):
        contact = super().save(commit=False)  # Memanfaatkan save() dari ModelForm
        if commit:
            contact.save()
        return contact

class IklanPromosiForm(forms.ModelForm):

    judul_iklan = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control", 'placeholder': 'Masukkan judul iklan'
            }
        )
    )
    deskripsi_iklan = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control", 'placeholder': 'Masukkan deskripsi iklan'
            }
        )
    )
    class Meta:
        model = IklanPromosi
        fields = ['judul_iklan', 'deskripsi_iklan']
    
    def save(self, commit=True):
        adv = super().save(commit=False)  # Memanfaatkan save() dari ModelForm
        if commit:
            adv.save()
        return adv
    

# class IklanUpdateForm(forms.ModelForm):
#     class Meta:
#         model = IklanPromosi
#         fields = ['judul_iklan', 'deskripsi_iklan']