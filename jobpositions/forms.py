from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'message']
from django import forms
from .models import Institutor

class InstitutorSignUpForm(forms.ModelForm):
    class Meta:
        model = Institutor
        fields = ['username', 'phone_number', 'email', 'password', 'repassword']
        widgets = {
            'password': forms.PasswordInput(),
            'repassword': forms.PasswordInput(),
        }
from django import forms

class InstitutorLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())
