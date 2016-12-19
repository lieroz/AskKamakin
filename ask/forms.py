from django import forms
from django.forms import ModelForm
from ask.models import Question


class SignUpForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", max_length=50,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))


class SignInForm(forms.Form):
    username = forms.CharField(label="Username", max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

