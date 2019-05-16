from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from Student.models import Student
from Teacher.models import Teacher

# Create your views here.

def index(request):
    return render(request, 'basic/index.html')


def user_selection(request):
    student = Student.objects.all().filter(user=request.user).first()
    if student != None:
        return HttpResponseRedirect(reverse('student:index'))
    else:
        teacher = Teacher.objects.all().filter(user=request.user).first()
        if teacher != None:
            return HttpResponseRedirect(reverse('teacher:index'))
        else:
            return HttpResponseRedirect(reverse('student:login'))


