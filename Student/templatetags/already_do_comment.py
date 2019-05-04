from django import template
from Examination.models import Multiple_Choice_Question
from Student.models import PaperResult, EssayComment

register = template.Library()

@register.simple_tag
def already_do_comment(student, essay_comments):
    for comment in essay_comments:
        if student.id == comment.student.id:
            return True
    
    return False
