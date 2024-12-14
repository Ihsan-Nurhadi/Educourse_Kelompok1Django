from django import forms
from .models import Order

class PaymentForm(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True)
    class Meta:
        model = Order
        fields = ['email']