from django.db import models
from django.contrib.auth.models import User
from Examination.models import Paper, Essay_Question
from GradeClass.models import GradeClass

# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    grade_class = models.ForeignKey(GradeClass, on_delete=models.CASCADE)
    paper_result = models.ManyToManyField(Paper, through='PaperResult')

    def __str__(self):
        return self.name


class PaperResult(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    choice_question_result = models.IntegerField(default=0)
    essay_question_result = models.IntegerField(default=0)
    does_choice_question_submit = models.BooleanField(default=False)
    does_essay_question_submit = models.BooleanField(default=False)
    submit_date = models.DateField(auto_now=True)

    def __str__(self):
        return "{} ( {} )".format(self.paper.title, self.student.name)


class EssayAnswer(models.Model):
    essay_question = models.ForeignKey(Essay_Question, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    student_answer = models.TextField()

    def __str__(self):
        return "{} - {} ({})".format(self.essay_question.paper.title, self.essay_question.title, student.name)


class EssayComment(models.Model):
    essay_answer = models.ForeignKey(EssayAnswer, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    score = models.IntegerField()