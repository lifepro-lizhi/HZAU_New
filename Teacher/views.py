from django.shortcuts import render
from django.urls import reverse
from Teacher.forms import UserRegisterForm, UserLoginForm, TeacherInfoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Examination.models import Paper
from Teacher.models import Teacher
from Student.models import PaperResult
from Video.models import Video
import csv

# Create your views here.

@login_required
def index(request):
    return render(request, 'teacher/index.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        teacher_info_form = TeacherInfoForm(data=request.POST)

        if user_form.is_valid() and teacher_info_form.is_valid():
            if request.POST['password'] == request.POST['confirm_password']:
                user = user_form.save()
                user.set_password(user.password)
                user.save()
            else:
                messages.warning(request, '两次密码输入不匹配，请重新输入！')
                return render(request, 'teacher/register.html')

            teacher_info = teacher_info_form.save(commit=False)
            teacher_info.user = user
            teacher_info.name = request.POST['name']
            teacher_info.save()

            registered = True

            messages.success(request, '注册成功！请返回重新登录')
            return render(request, 'basic/index.html')
        else:
            errors = user_form.errors.as_data()
            for key in errors.keys():
                messages.warning(request, errors[key])
            return render(request, 'teacher/register.html')
    else:
        user_form = UserRegisterForm()
        teacher_info_form = TeacherInfoForm()
        
        context = {'user_form': user_form,
                   'teacher_info_form': teacher_info_form,
                   'registered': registered}
        return render(request, 'teacher/register.html', context=context)


def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            try:
                teacher = Teacher.objects.get(user=user)
            except Teacher.DoesNotExist:
                messages.warning(request, '用户名或密码错误！')
                return HttpResponseRedirect(reverse('basic:index'))

            if user.is_active:
                login(request, user)
                # messages.success(request, '登录成功！')
                return HttpResponseRedirect(reverse('teacher:index'))
            else:
                messages.warning(request, '用户不处于活跃状态')
                return HttpResponseRedirect(reverse('basic:index'))
        else:
            messages.warning(request, '用户名或密码错误！')
            return HttpResponseRedirect(reverse('basic:index'))
    else:
        return render(request, 'teacher/login.html')


@login_required
def teacher_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic:index'))


@login_required
def teacher_papers(request):
    papers = Paper.objects.filter(paper_maker=request.user.teacher)
    context = {'papers': papers}
    return render(request, 'teacher/papers.html', context=context)


@login_required
def uploaded_videos(request):
    videos = Video.objects.filter(teacher=request.user.teacher)
    context = {'videos': videos}
    return render(request, 'teacher/uploaded_videos.html', context=context)


@login_required
def paper_results_list(request):
    teacher = Teacher.objects.filter(user=request.user)
    papers = Paper.objects.filter(paper_maker__in=teacher, is_published=True)
    paper_results = []
    for paper in papers:
        result = PaperResult.objects.filter(paper=paper)
        paper_results.append(result)

    papers_result_list = zip(papers, paper_results)
    context = {'papers_result_list': papers_result_list}
    return render(request, 'teacher/paper_results_list.html', context=context)


@login_required
def export_paper_results(request, paper_id):
    paper = Paper.objects.get(pk=paper_id)
    paper_results = list(PaperResult.objects.filter(paper=paper, does_choice_question_submit=True, does_essay_question_submit=True))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="result_csv.csv"'

    writer = csv.writer(response)
    writer.writerow(['学号', '学生姓名', '班级', '总分数', '选择题得分', '问答题得分', '提交时间'])

    for result in paper_results:
        writer.writerow([result.student.student_id, result.student.name, result.student.grade_class.title, 
                         result.essay_question_result + result.choice_question_result, 
                         result.choice_question_result, 
                         result.essay_question_result,
                         result.submit_date])
    return response

    

