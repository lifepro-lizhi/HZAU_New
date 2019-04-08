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


# collection of essay_answers for specific paper and student
class PaperAnswer(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    comments_count = models.IntegerField(default=0)


# one single essay_answer for specific essay_question and student
class EssayAnswer(models.Model):
    paper_answer = models.ForeignKey(PaperAnswer, on_delete=models.SET_NULL, null=True)
    essay_question = models.ForeignKey(Essay_Question, on_delete=models.SET_NULL, null=True)
    student_answer = models.TextField()

    def __str__(self):
        return "{} - {} ({})".format(self.essay_question.paper.title, self.essay_question.title, student.name)


# comment for specific essay_answer
class EssayComment(models.Model):
    essay_answer = models.ForeignKey(EssayAnswer, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True)
    score = models.IntegerField(default=0, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

        paper_answer = self.essay_answer.paper_answer
        total_score = 0
        for essay_answer in list(paper_answer.essayanswer_set.all()):
            score = 0
            comments_count = essay_answer.essaycomment_set.count()
            print('comments_count: {}'.format(comments_count))
            if comments_count != 0:
                for essay_comment in list(essay_answer.essaycomment_set.all()):
                    print(essay_comment.score)
                    score += essay_comment.score
                score = score / comments_count
                total_score += score
        
        paper_result = PaperResult.objects.filter(paper=paper_answer.paper, student=paper_answer.student).first()
        if paper_result == None:
            paper_result = PaperResult()
            paper_result.paper = paper_answer.paper
            paper_result.student = paper_answer.student
        
        print('total_score: {}'.format(total_score))
        paper_result.essay_question_result = total_score
        paper_result.save()
