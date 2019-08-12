from django.shortcuts import render, redirect
from History.models import HistoryRecord
from datetime import date

# Create your views here.

def record_access_history(request, user_type, name):
    record = HistoryRecord()
    record.name = name
    record.user_type = user_type
    record.access_date = date.today()

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ipaddress = x_forwarded_for.split(',')[-1].strip()
    else:
        ipaddress = request.META.get('REMOTE_ADDR')

    record.ip_address = ipaddress

    record.save()


def list_records(request):
    total_count = len(HistoryRecord.objects.all())
    teacher_count = len(HistoryRecord.objects.all().filter(user_type="教师"))
    student_count = len(HistoryRecord.objects.all().filter(user_type="学生"))
    guest_count = len(HistoryRecord.objects.all().filter(user_type="游客"))
    context = {'total_count' : total_count,
               'teacher_count' : teacher_count,
               'student_count' : student_count,
               'guest_count' : guest_count}
    return render(request, 'history/list_record.html', context)


def recent_records_detail(request):
    records = HistoryRecord.objects.all().order_by('-access_date')
    context = {'records' : records}
    return render(request, 'history/recent_records_detail.html', context)



    