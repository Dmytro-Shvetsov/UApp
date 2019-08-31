from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django import forms
from .models import UserProfile


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


class ChangePasswordForm(SetPasswordForm):
    old_password = forms.CharField(
        max_length=50, widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Password'})
    )
    new_password1 = forms.CharField(
        max_length=50, widget=forms.PasswordInput({
            'class': 'form-control',
            'placeholder': 'Password'})
    )

    new_password2 = forms.CharField(
        max_length=50, widget=forms.PasswordInput(
            {'class': 'form-control',
             'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class UpdateUserProfileForm(forms.Form):
    first_name = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput({
            'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput({
            'class': 'form-control'})
    )

    bio = forms.CharField(
        max_length=5000, required=False, widget=forms.Textarea({
            'class': 'form-control'})
    )

    company = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput({
            'class': 'form-control'})
    )

    current_position = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput({
            'class': 'form-control'})
    )

    user_email_is_public = forms.BooleanField(required=False, widget=forms.CheckboxInput({
            'class': 'custom-control-input'})
    )

    image = forms.ImageField(required=True)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'bio', 'company', 'current_position', 'user_email_is_public', 'image')
