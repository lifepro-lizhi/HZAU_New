from django import forms
from Video.models import Video, Image

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = {'title', 'video'}
        

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = {'title', 'image'}