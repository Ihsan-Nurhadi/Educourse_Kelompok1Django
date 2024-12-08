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
class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('post', 'class_name', 'text', 'video')  # Tambahkan 'post'
        widgets = {
            'class_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'video': forms.URLInput(attrs={'class': 'form-control'}),
            'post': forms.Select(attrs={'class': 'form-control'}),  # Styling select input
        }

    def __init__(self, *args, **kwargs):
        # Ambil user dari kwargs dan hapus agar tidak ada error
        user = kwargs.pop('user', None)
        super(ClassForm, self).__init__(*args, **kwargs)
        
        # Filter queryset untuk field 'post' agar hanya mencakup postingan milik user (guru)
        if user is not None:
            self.fields['post'].queryset = Post.objects.filter(author=user)
