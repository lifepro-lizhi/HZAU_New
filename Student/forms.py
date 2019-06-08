from django import forms
from django.contrib.auth.models import User
from Student.models import Student
from GradeClass.models import GradeClass


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


class StudentInfoForm(forms.ModelForm):
    name = forms.CharField(max_length=10)
    student_id = forms.CharField(max_length=20)
    grade_class = forms.ModelChoiceField(queryset=GradeClass.objects.all())

    GENDER_CHOICES = [
        ('male', '男'),
        ('female', '女'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    phone = forms.CharField(max_length=20)

    class Meta():
        model = Student
        fields = ('name', 'student_id', 'grade_class', 'gender', 'phone')