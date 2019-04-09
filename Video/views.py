from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from Video.forms import VideoForm
from Video.models import Video
from Teacher.models import Teacher
from datetime import date
from django.contrib import messages
import os, sys, stat

# Create your views here.

def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = Teacher.objects.get(user=request.user)
            video_instance = form.save(commit=False)
            video_instance.teacher = teacher
            video_instance.upload_date = date.today()
            video_instance.save()

            os.chmod(video_instance.video.path, stat.S_IROTH | stat.S_IXOTH)

            return render(request, 'teacher/index.html')
    else:
        form = VideoForm()
        context = {'form': form}
        return render(request, 'video/upload_video.html', context=context)


def video_list(request):
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, 'video/video_list.html', context=context)


def video_play(request, video_id):
    video = Video.objects.get(pk=video_id)
    url = video.video.url
    context = {'url': url}
    return render(request, 'video/video_play.html', context=context)


def video_manage(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        raise Http404("Video does not exist")
    
    context = {'video': video}
    return render(request, 'video/video_manage.html', context=context)


def video_title_modify(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        raise Http404("Video does not exist")

    if request.method == 'POST':
        title = request.POST['title']
        
        video.title = title
        video.save()

        messages.success(request, '视频标题修改成功！')
        context = {'video': video}
        return render(request, 'video/video_manage.html', context=context)
    else:
        context = {'video': video}
        return render(request, 'video/video_title_modify.html', context=context)


def video_delete(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        raise Http404("Video does not exist")
    
    if request.method == 'POST':
        try:
            os.remove(video.video.path)
            video.delete()
        except:
            video.delete()

        messages.success(request, '视频删除成功！')
        return HttpResponseRedirect(reverse('video:video_list'))
    else:
        context = {'video': video}
        return render(request, 'video/video_delete.html', context=context)
    





