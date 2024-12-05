from django import forms
from .models import Post , Class

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'video','thumbnail','price' )
        widgets = {
            'title': forms.TextInput(attrs={'class':'textinputclass'}),
        }
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('class_name','text','video') 