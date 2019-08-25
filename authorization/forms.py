from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=254, widget=forms.TextInput(
            {'class': 'form-control',
             'placeholder': 'Enter your user name'})
    )

    email = forms.EmailField(
        max_length=254, widget=forms.TextInput(
            {'class': 'form-control',
             'placeholder': 'Enter your email address'})
    )

    password1 = forms.CharField(
        max_length=50, widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Password'})
    )

    password2 = forms.CharField(
        max_length=50, widget=forms.PasswordInput(
            {'class': 'form-control',
             'placeholder': 'Confirm Password'})
    )
