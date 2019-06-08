from django.shortcuts import render, redirect
from django.urls import reverse
from Teacher.forms import UserRegisterForm, UserLoginForm, TeacherInfoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, FileResponse 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Examination.models import Paper
from Teacher.models import Teacher
from Student.models import Student, PaperResult
from GradeClass.models import GradeClass
from Video.models import Video
import csv
import io
from reportlab.pdfgen import canvas

# Create your views here.

@login_required
def index(request):
    return render(request, 'teacher/index.html')


def register(request):
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
            teacher_info.phone = request.POST['phone']
            teacher_info.save()

            messages.success(request, '注册成功！请返回重新登录')
            return HttpResponseRedirect(reverse('basic:user_login'))
        else:
            errors = user_form.errors.as_data()
            for key in errors.keys():
                messages.warning(request, errors[key])
            return HttpResponseRedirect(reverse('teacher:register'))
    else:
        user_form = UserRegisterForm()
        teacher_info_form = TeacherInfoForm()
        
        context = {'user_form': user_form,
                   'teacher_info_form': teacher_info_form}
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
                return HttpResponseRedirect(reverse('basic:user_login'))

            if user.is_active:
                login(request, user)
                # messages.success(request, '登录成功！')
                return HttpResponseRedirect(reverse('teacher:index'))
                # return redirect('http://144.202.122.52/unity_index.html')
            else:
                messages.warning(request, '用户不处于活跃状态')
                return HttpResponseRedirect(reverse('basic:user_login'))
        else:
            messages.warning(request, '用户名或密码错误！')
            return HttpResponseRedirect(reverse('basic:user_login'))
    else:
        return render(request, 'teacher/login.html')


@login_required
def teacher_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic:user_login'))


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
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(paper.title)

    writer = csv.writer(response)
    writer.writerow(['学号', '学生姓名', '班级', '总分数', '选择题得分', '问答题得分', '提交时间'])

    for result in paper_results:
        writer.writerow([result.student.student_id, result.student.name, result.student.grade_class.title, 
                         result.essay_question_result + result.choice_question_result, 
                         result.choice_question_result, 
                         result.essay_question_result,
                         result.submit_date])
    return response

    
@login_required
def export_paper_to_pdf(request, paper_id):
    paper = Paper.objects.get(pk=paper_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    # p.drawCentredString(1, 1, paper.title)
    p.drawString(100, 100, paper.title)
    
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    # return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
    return response


@login_required
def teacher_personal_info(request):
    teacher = Teacher.objects.get(user=request.user)
    context = {'teacher': teacher}
    return render(request, 'teacher/teacher_personal_info.html', context=context)


@login_required
def modify_personal_info(request):
    teacher = Teacher.objects.get(user=request.user)
    if request.method == 'POST':
        teacher_info_form = TeacherInfoForm(data=request.POST)
        
        if teacher_info_form.is_valid():
            teacher.user.email = request.POST['email']
            teacher.name = request.POST['name']
            teacher.phone = request.POST['phone']
            teacher.user.save()
            teacher.save()

            messages.success(request, '个人信息修改成功！')
            return HttpResponseRedirect(reverse('teacher:teacher_personal_info'))
        else:
            errors = user_form.errors.as_data()
            for key in errors.keys():
                messages.warning(request, errors[key])

            return HttpResponseRedirect(reverse('teacher:modify_personal_info'))
    else:
        return render(request, 'teacher/modify_personal_info.html')


def reset_password(request):
    teacher = Teacher.objects.get(user=request.user)

    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            teacher.user.set_password(request.POST['password'])
            teacher.user.save()
            messages.success(request, '修改密码成功！请返回重新登录')
            return HttpResponseRedirect(reverse('teacher:teacher_personal_info'))
        else:
            messages.warning(request, '两次密码输入不匹配，请重新输入！')
            return HttpResponseRedirect(reverse('teacher:reset_password'))
    else:
        return render(request, 'teacher/reset_password.html')


@login_required
def grade_class_list(request):
    grade_class = GradeClass.objects.all()
    context = {'grade_class': grade_class}
    return render(request, 'teacher/grade_class_list.html', context=context)


@login_required
def grade_class_detail(request, gradeclass_id):
    try:
        grade_class = GradeClass.objects.get(pk=gradeclass_id)
    except GradeClass.DoesNotExist:
        messages.warning(request, '专业班级不存在！')
        return HttpResponseRedirect(reverse('teacher:grade_class_list'))
    
    students = Student.objects.all().filter(grade_class=grade_class)
    context = {'grade_class': grade_class,
               'students': students}
    return render(request, 'teacher/grade_class_detail.html', context=context)


@login_required
def export_grade_class_detail(request, gradeclass_id):
    try:
        grade_class = GradeClass.objects.get(pk=gradeclass_id)
    except GradeClass.DoesNotExist:
        messages.warning(request, '专业班级不存在！')
        return HttpResponseRedirect(reverse('teacher:grade_class_list'))
    
    students = Student.objects.all().filter(grade_class=grade_class)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(grade_class.title)

    writer = csv.writer(response)
    writer.writerow(['学生姓名', '学号', '专业班级', '性别', '电话', '邮箱'])

    for student in students:
        writer.writerow([student.name, student.student_id, student.grade_class.title, 
                         student.get_gender_display(), student.phone, student.user.email])
    return response