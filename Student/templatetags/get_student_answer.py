from django import template
from Examination.models import Multiple_Choice_Question
from Student.models import PaperResult

register = template.Library()

@register.simple_tag
def get_student_answer(question_id, student_answers):
    id_str = str(question_id)
    if id_str in student_answers:
        return student_answers[id_str]
    else:
        return "未选择"
    
@register.simple_tag
def get_right_or_wrong(question_id, student_answers):
    question = Multiple_Choice_Question.objects.get(pk=question_id)

    id_str = str(question_id)
    print("id: {}".format(id_str))
    if id_str in student_answers:
        print("aa: {}".format(student_answers[id_str]))
        print(question.right_answer)
        if student_answers[id_str] == question.right_answer:
            return True
        else:
            return False
    else:
        return False


@register.simple_tag
def get_paper_result_choice_question_status(paper_result):
    print(paper_result)
    # if paper_result is not None:
    #     if paper_result.does_choice_question_submit == True:
    #         return "已提交，分数：{}".format(paper_result.choice_question_result)
    #     else:
    #         return "未提交"
    # else:
    #     return "未提交"


@register.simple_tag
def get_paper_result_essay_question_status(paper_result):
    print(paper_result)
    # if paper_result is not None:
    #     if paper_result.does_essay_question_submit == True:
    #         return "已提交，分数：{}".format(paper_result.essay_question_result)
    #     else:
    #         return "未提交"
    # else:
    #     return "未提交"


