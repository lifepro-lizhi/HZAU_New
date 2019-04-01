from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from Student.forms import UserLoginForm, UserRegisterForm, StudentInfoForm
from Examination.models import Paper, Multiple_Choice_Question, Essay_Question
from Student.models import Student, PaperResult, EssayAnswer, PaperAnswer
from GradeClass.models import GradeClass
from Video.models import Video
from datetime import date
import random

# Create your views here.

def index(request):
    return render(request, 'student/index.html')
    # return render(request, 'basic/sidebar_base.html')


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        student_info_form = StudentInfoForm(data=request.POST)

        if user_form.is_valid() and student_info_form.is_valid():
            if request.POST['password'] == request.POST['confirm_password']:
                user = user_form.save()
                user.set_password(user.password)
                user.save()
            else:
                messages.warning(request, '两次密码输入不匹配，请重新输入！')
                return render(request, 'student/register.html')

            student_info = student_info_form.save(commit=False)
            student_info.user = user
            student_info.name = request.POST['name']
            student_info.student_id = request.POST['student_id']

            grade_class_pk = request.POST['grade_class']
            grade_class = GradeClass.objects.get(pk=grade_class_pk)
            student_info.grade_class = grade_class
            student_info.save()

            registered = True

            messages.success(request, '注册成功！请返回重新登录')
            return render(request, 'basic/index.html')
        else:
            errors = user_form.errors.as_data()
            for key in errors.keys():
                messages.warning(request, errors[key])

            user_form = UserRegisterForm()
            student_info_form = StudentInfoForm()
            grade_class = GradeClass.objects.all()
            context = {'user_form': user_form,
                   'student_info_form': student_info_form,
                   'grade_class': grade_class,
                   'registered': registered}
            return render(request, 'student/register.html', context=context)
    else:
        user_form = UserRegisterForm()
        student_info_form = StudentInfoForm()
        grade_class = GradeClass.objects.all()

        context = {'user_form': user_form,
                   'student_info_form': student_info_form,
                   'grade_class': grade_class,
                   'registered': registered}
        return render(request, 'student/register.html', context=context)


def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # messages.success(request, '登录成功！')
                return HttpResponseRedirect(reverse('student:index'))
            else:
                messages.warning(request, '用户不处于活跃状态')
                return HttpResponseRedirect(reverse('basic:index'))
        else:
            messages.warning(request, '用户名或密码错误！')
            return HttpResponseRedirect(reverse('basic:index'))
    else:
        return render(request, 'teacher/login.html')


@login_required
def student_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic:index'))


def paper_list(request, showEssayComment):
    papers = Paper.objects.filter(is_published__exact=True)
    context = {'papers' : papers,
               'showEssayComment' : showEssayComment}
    return render(request, 'student/paper_list.html', context=context)


def paper_info(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")
    
    student = Student.objects.get(user=request.user)
    paper_result = PaperResult.objects.all().filter(paper=paper, student=student)
    if len(paper_result) == 0:
        context = {'paper': paper,
                   'paper_result': None}
    else:
        context = {'paper': paper,
                   'paper_result': paper_result[0]}
    
    return render(request, 'student/paper_info.html', context=context)


def do_paper_type_choose(request, paper_id):
    paper = Paper.objects.get(pk=paper_id)
    context = {'paper': paper}
    return render(request, 'student/do_paper_type_choose.html', context)


def do_paper_multiple_choice(request, paper_id):
    if request.method == 'POST':
        score = 0
        answers = {}
        for key in request.POST.keys():
            if 'question' in key:
                question_id = int(key[key.find('.') + 1 :])
                answer = request.POST[key]
                question = Multiple_Choice_Question.objects.get(pk=question_id)
                if answer == question.right_answer:
                    score += question.point

                answers[str(question_id)] = answer

        paper = Paper.objects.get(pk=paper_id)
        # student = Student.objects.all().filter(user=request.user)
        student = Student.objects.get(user=request.user)
        if student is not None:
            print("name: {}".format(student.name))
            print("id: {}".format(student.student_id))
        paper_result = PaperResult(paper=paper, student=student, submit_date=date.today())
        paper_result.choice_question_result = score
        paper_result.does_choice_question_submit = True
        paper_result.save()

        context = {'paper': paper, 
                   'answers': answers, 
                   'paper_result': paper_result, 
                   'is_essay_result': False}
        return render(request, 'student/do_paper_result.html', context)
    else:
        paper = Paper.objects.get(pk=paper_id)
        student = Student.objects.get(user=request.user)
        paper_result = PaperResult.objects.all().filter(paper=paper, student=student)
        if len(paper_result) == 0:
            context = {'paper': paper}
            return render(request, 'student/do_paper_multiple_choice.html', context)
        else:
            context = {'paper': paper, 
                       'answers': None,
                       'paper_result': paper_result[0]}
            return render(request, 'student/do_paper_result.html', context)


def do_paper_essay(request, paper_id):
    paper = Paper.objects.get(pk=paper_id)
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        paper_answer = PaperAnswer()
        paper_answer.paper = paper
        paper_answer.student = student
        paper_answer.save()

        answers = []

        for key in request.POST.keys():
            print('111')
            print(key)
            if 'question' in key:
                print('222')
                question_id = int(key[key.find('.') + 1 :])
                question = Essay_Question.objects.get(pk=question_id)
                print('333')

                answer_text = request.POST[key]
                answers.append(answer_text)

                answer = EssayAnswer()
                answer.essay_question = question
                answer.paper_answer = paper_answer
                answer.student_answer = answer_text
                answer.save()
                print('444')
        
        essay_questions = paper.essay_question_set.all()
        print(len(essay_questions))
        print(len(answers))
        questions_and_answers = zip(essay_questions, answers)
        context = {'paper': paper, 
                   'questions_and_answers': questions_and_answers,
                   'is_essay_result': True}
        return render(request, 'student/do_paper_result.html', context)
    else:
        paper = Paper.objects.get(pk=paper_id)
        context = {'paper': paper}
        return render(request, 'student/do_paper_essay.html', context)


def paper_results(request):
    student = Student.objects.get(user=request.user)
    results = PaperResult.objects.filter(student=student)

    context = {'results': results}
    return render(request, 'student/paper_results.html', context)


def video_list(request):
    videos = Video.objects.all()
    context = {'videos': videos}

    return render(request, 'student/video_list.html', context=context)


def essay_comment_pick(request, paper_id):
    paper = Paper.objects.get(pk=paper_id)
    context = {'paper': paper}

    return render(request, 'student/essay_comment_pick.html', context=context)


def pick_random_paper(request, paper_id):
    paper = Paper.objects.get(pk=paper_id)
    paper_commits_count = len(paper.paperanswer_set.all()) / paper.essay_question_count
    paper_answers_to_add_comment = []
    already_picked_index = []

    if paper_commits_count > 5:
        while len(comments_for_paperanswer) < 5:    # one student should do at least 5 comments
            r = random.randint(0, paper_commits_count)    # random pick a index
            if r not in already_picked_index:    # insure the current index has not been selected 
                paper_answer = paper.paperanswer_set.order_by('id')[r]    # get the paper_answer at the specified index
                if paper_answer.comments_count < 5:    # insure the paper_answer's comments' count is less than 5
                    paper_answers_to_add_comment.append(paper_answer)
                else:
                    continue
            else:
                continue
    
    context = {'paper': paper,
               'paper_answers': paper_answers_to_add_comment}
    return render(request, 'student/do_comment_paper_list.html', context=context)







