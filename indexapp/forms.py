from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from taskapp.models import User


class LoginForm(forms.Form):
    username_or_email = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter username or email','class':'form-control', }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Enter password','class':'form-control',}))


class UserPasswordResetForm(SetPasswordForm):

    new_password1 = forms.CharField(label='Password',
        help_text="<ul class='errorlist text-muted'><li>Your password can 't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can 't be a commonly used password.</li> <li>Your password can 't be entirely numeric.<li></ul>",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'type': 'password',
            'id': 'user_password',
        }))

    new_password2 = forms.CharField(label='Confirm password',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'confirm password',
            'type': 'password',
            'id': 'user_password',
        }))


class UserForgotPasswordForm(PasswordResetForm):

    email = forms.EmailField(label='Email address',
        max_length=254,
        required=True,
        widget=forms.TextInput(
         attrs={'class': 'form-control',
                'placeholder': 'email address',
                'type': 'text',
                'id': 'email_address'
                }
        ))

