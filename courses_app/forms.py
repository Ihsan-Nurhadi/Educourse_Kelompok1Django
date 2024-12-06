from django import forms
from .models import Post , Class

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'video', 'thumbnail', 'price')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'video': forms.URLInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# forms.py
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('post','class_name', 'text', 'video')  # Tambahkan 'post'
        widgets = {
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'video': forms.URLInput(attrs={'class': 'form-control'}),
            'post': forms.Select(attrs={'class': 'form-control'}),  # Styling select input
        }
