from django import forms
from Video.models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = {'title', 'video'}