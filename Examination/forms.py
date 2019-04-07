from django import forms
from Examination.models import Paper, Multiple_Choice_Question, Essay_Question


class DateInput(forms.DateInput):
    input_type = 'date'


class PaperForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'description', 'expire_date', 'is_published'] 
        widgets = {'expire_date': forms.SelectDateWidget()}


class MultipleChoiceQuestionForm(forms.ModelForm):
    class Meta:
        model = Multiple_Choice_Question
        exclude = ['paper']


class EssayQuestionForm(forms.ModelForm):
    class Meta:
        model = Essay_Question
        exclude = ['paper']
