from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
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

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254, widget=forms.TextInput(
            {'class': 'form-control',
             'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Enter your password'})
    )


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254, widget=forms.TextInput(
            {'class': 'form-control',
             'placeholder': 'Enter your email address'})
    )


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Password'}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            {'class': 'form-control',
                'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('new_password1', 'new_password2')
