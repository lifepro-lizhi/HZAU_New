from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from Examination.forms import PaperForm, MultipleChoiceQuestionForm, EssayQuestionForm
from Examination.models import Paper, Multiple_Choice_Question, Essay_Question
from Student.models import PaperResult
from datetime import date
from django.contrib import messages
from Teacher.models import Teacher

# Create your views here.

def create_paper(request):
    if request.method == 'POST':
        form = PaperForm(request.POST)

        if form.is_valid():
            paper = form.save(commit=False)
            paper.paper_maker = request.user.teacher
            paper.save()
            messages.success(request, '试卷创建成功！')
            return HttpResponseRedirect(reverse('examination:paper_info', args=[paper.pk]))
        else:
            print(form.errors)
    else:
        form = PaperForm()
        context = {'form' : form}
        return render(request, 'examination/create_paper.html', context=context)


def choose_create_type(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")

    context = {'paper' : paper}
    return render(request, 'examination/choose_create_type.html', context)


def create_multiple_choice_question(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")

    if request.method == 'POST':
        form = MultipleChoiceQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.paper = paper
            question.save()

            messages.success(request, '选择题添加成功！')

            context = {'paper' : paper}
            if request.POST['save'] == 'just_save':
                return render(request, 'examination/paper_info.html', context=context)
            elif request.POST['save'] == "save_and_continue":
                form = MultipleChoiceQuestionForm()
                context = {'form' : form, 'paper' : paper}
                return render(request, 'examination/create_multiple_choice_question.html', context=context)
        else:
            print(form.errors)
    else:
        form = MultipleChoiceQuestionForm()
        context = {'form' : form, 'paper' : paper}
        return render(request, 'examination/create_multiple_choice_question.html', context=context)


def create_essay_question(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")
    
    if request.method == 'POST':
        form = EssayQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.paper = paper
            question.save()

            messages.success(request, '问答题添加成功！')

            context = {'paper' : paper}
            if request.POST['save'] == 'just_save':
                return render(request, 'examination/paper_info.html', context=context)
            elif request.POST['save'] == "save_and_continue":
                form = EssayQuestionForm()
                context = {'form' : form, 'paper' : paper}
                return render(request, 'examination/create_essay_question.html', context=context)
        else:
            print(form.errors)
    else:
        form = EssayQuestionForm()
        context = {'form' : form, 'paper': paper}
        return render(request, 'examination/create_essay_question.html', context=context)


def paper_list(request):
    teacher = Teacher.objects.get(user=request.user)
    papers_published = Paper.objects.filter(is_published__exact=True, paper_maker=teacher)
    papers_unpublished = Paper.objects.filter(is_published__exact=False, paper_maker=teacher)
    context = {'papers_published' : papers_published, 'papers_unpublished' : papers_unpublished}
    return render(request, 'examination/paper_list.html', context=context)


def paper_detail(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")
    
    context = {'paper' : paper}
    return render(request, 'examination/paper_detail.html', context=context)


def paper_preview(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")
    
    context = {'paper' : paper}
    return render(request, 'examination/paper_preview.html', context=context)


def modify_multiple_choice_question(request, question_id):
    try:
        question = Multiple_Choice_Question.objects.get(pk=question_id)
    except Multiple_Choice_Question.DoesNotExist:
        raise Http404("Question does not exist")
    
    if request.method == 'POST':
        form = MultipleChoiceQuestionForm(request.POST)
        if form.is_valid():
            question.title = form.cleaned_data['title']
            question.option_A = form.cleaned_data['option_A']
            question.option_B = form.cleaned_data['option_B']
            question.option_C = form.cleaned_data['option_C']
            question.option_D = form.cleaned_data['option_D']
            question.point = form.cleaned_data['point']
            question.right_answer = form.cleaned_data['right_answer']
            question.save()

            messages.success(request, '修改成功！')

            return HttpResponseRedirect(reverse('examination:paper_preview', args=[question.paper.pk]))
        else:
            print(form.errors)
    else:
        form = MultipleChoiceQuestionForm(instance=question)
        context = {'form' : form, 'question' : question}
        return render(request, 'examination/modify_multiple_choice_question.html', context=context)

def modify_essay_question(request, question_id):
    try:
        question = Essay_Question.objects.get(pk=question_id)
    except Essay_Question.DoesNotExist:
        raise Http404("Question does not exist")
    
    if request.method == 'POST':
        form = EssayQuestionForm(request.POST)
        if form.is_valid():
            question.title = form.cleaned_data['title']
            question.point = form.cleaned_data['point']
            question.right_answer = form.cleaned_data['right_answer']
            question.save()

            messages.success(request, '修改成功！')

            return HttpResponseRedirect(reverse('examination:paper_preview', args=[question.paper.pk]))
        else:
            print(form.errors)
    else:
        form = EssayQuestionForm(instance=question)
        context = {'form' : form, 'question' : question}
        return render(request, 'examination/modify_essay_question.html', context=context)


def modify_paper(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")
    
    if request.method == 'POST':
        form = PaperForm(request.POST)
        if form.is_valid():
            paper.title = form.cleaned_data['title']
            paper.description = form.cleaned_data['description']
            paper.expire_date = form.cleaned_data['expire_date']
            paper.save()
            messages.success(request, '试卷修改成功！')

            return HttpResponseRedirect(reverse('examination:paper_list'))
        else:
            print(form.errors)
    else:
        form = PaperForm(instance=paper)
        context = {'form' : form, 'paper' : paper}
        return render(request, 'examination/modify_paper.html', context=context)


def publish_paper(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")
    
    paper.is_published = True
    paper.publish_date = date.today()
    paper.save()

    messages.success(request, '试卷发布成功！')

    return HttpResponseRedirect(reverse('examination:paper_list'))


def delete_paper(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")
    
    if request.method == 'POST':
        paper = Paper.objects.get(pk=paper_id)
        paper.delete()

        messages.success(request, '试卷删除成功！')
        return HttpResponseRedirect(reverse('examination:paper_list'))
    else:
        if paper.paper_maker == request.user.teacher:
            context = {'paper': paper}
            return render(request, 'examination/paper_delete.html', context=context)
        else:
            messages.success(request, '该试卷不是由您所创建，您没有权限删除！')
            return HttpResponseRedirect(reverse('examination:paper_info', args=[paper.pk]))


def paper_info(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")
    
    context = {'paper': paper}
    return render(request, 'examination/paper_info.html', context=context)


def paper_results(request, paper_id):
    try:
        paper = Paper.objects.get(pk=paper_id)
    except Paper.DoesNotExist:
        raise Http404("Paper does not exist")
    
    results = PaperResult.objects.filter(paper=paper)
    context = {'results': results, 'paper': paper}
    return render(request, 'examination/paper_results.html', context=context)
