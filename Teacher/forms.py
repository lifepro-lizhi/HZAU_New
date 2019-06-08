from django import forms
from django.contrib.auth.models import User
from Teacher.models import Teacher


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password', 'email')


class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'password')


class TeacherInfoForm(forms.ModelForm):
    name = forms.CharField(max_length=10)
    phone = forms.CharField(max_length=20)

    class Meta():
        model = Teacher
        fields = ('name', 'phone')