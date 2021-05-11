from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User,Profile, Address
from allauth.account.forms import LoginForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email')



class UserRegisterForm(UserCreationForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['name','email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['name','email']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address','image']


# create forms to extend allauth

# ACCOUNT_FORMS = {'login': 'yourapp.forms.YourLoginForm'} -- needs to be added to settings.py


class UserLoginForm(LoginForm):
    email = forms.EmailField(),

    class Meta:
        model = User
        fields = ['email', 'password']




