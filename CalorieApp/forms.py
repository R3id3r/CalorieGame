from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Player
from django import forms
from django.forms.widgets import PasswordInput, TextInput

class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = Player
        fields = ['username', 'email', 'password1', 'password2']

class AuthenticateUserForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
        