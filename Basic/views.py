from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from Student.models import Student
from Teacher.models import Teacher
from History.models import HistoryRecord
from History.views import record_access_history
from datetime import date

# Create your views here.

def index(request):
    return render(request, 'basic/index.html')


def user_selection(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse('basic:user_login'))

    student = Student.objects.all().filter(user=request.user).first()
    if student != None:
        return HttpResponseRedirect(reverse('student:index'))
    else:
        teacher = Teacher.objects.all().filter(user=request.user).first()
        if teacher != None:
            return HttpResponseRedirect(reverse('teacher:index'))
        else:
            return HttpResponseRedirect(reverse('basic:user_login'))


def user_login(request):
    return render(request, 'student/login.html')


def guest_login(request):
    return render(request, 'basic/guest.html')


def guest_name(request):
    if request.method == 'POST':
        if request.POST['guest_name'] is not "":
            record_access_history(request, "游客", request.POST['guest_name'])
            return redirect('http://211.69.130.114:8000/bird/index.html')


def start(request):
    return render(request, 'basic/start_page.html')


