from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from Video.forms import VideoForm, ImageForm
from Video.models import Video, Image
from Teacher.models import Teacher
from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os, sys, stat

# Create your views here.

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = Teacher.objects.get(user=request.user)
            video_instance = form.save(commit=False)
            video_instance.teacher = teacher
            video_instance.upload_date = date.today()
            video_instance.save()

            os.chmod(video_instance.video.path, stat.S_IRWXO | stat.S_IRWXU | stat.S_IRWXG)

            return HttpResponseRedirect(reverse('video:media_list'))
    else:
        form = VideoForm()
        context = {'form': form}
        return render(request, 'video/upload_video.html', context=context)


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = Teacher.objects.get(user=request.user)
            image_instance = form.save(commit=False)
            image_instance.teacher = teacher
            image_instance.upload_date = date.today()
            image_instance.save()

            os.chmod(image_instance.image.path, stat.S_IRWXO | stat.S_IRWXU | stat.S_IRWXG)

            return HttpResponseRedirect(reverse('video:media_list'))
    else:
        form = ImageForm()
        context = {'form': form}
        return render(request, 'video/upload_image.html', context=context)


@login_required
def media_list(request):
    videos = Video.objects.all()
    images = Image.objects.all()
    context = {'videos': videos,
               'images': images}
    return render(request, 'video/media_list.html', context=context)


@login_required
def video_play(request, video_id):
    video = Video.objects.get(pk=video_id)
    url = video.video.url
    
    is_teacher = False
    teacher = Teacher.objects.all().filter(user=request.user).first()
    if teacher != None:
        is_teacher = True
    else:
        is_teacher = False

    context = {'url': url,
               'is_teacher': is_teacher}
    return render(request, 'video/video_play.html', context=context)

@login_required
def image_play(request, image_id):
    image = Image.objects.get(pk=image_id)
    url = image.image.url

    is_teacher = False
    teacher = Teacher.objects.all().filter(user=request.user).first()
    if teacher != None:
        is_teacher = True
    else:
        is_teacher = False;

    context = {'url': url,
               'is_teacher': is_teacher}
    return render(request, 'video/image_play.html', context=context)


@login_required
def video_manage(request, video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        raise Http404("Video does not exist")
    
    context = {'video': video}
    return render(request, 'video/video_manage.html', context=context)

@login_required
def image_manage(request, image_id):
    try:
        image = Image.objects.get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404("Image does not exist")
    
    context = {'image': image}
    return render(request, 'video/image_manage.html', context=context)


@login_required
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


@login_required
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
        return HttpResponseRedirect(reverse('video:media_list'))
    else:
        context = {'video': video}
        return render(request, 'video/video_delete.html', context=context)


@login_required
def image_title_modify(request, image_id):
    try:
        image = Image.objects.get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404("Image does not exist")

    if request.method == 'POST':
        title = request.POST['title']
        
        image.title = title
        image.save()

        messages.success(request, '图片标题修改成功！')
        context = {'image': image}
        return render(request, 'video/image_manage.html', context=context)
    else:
        context = {'image': image}
        return render(request, 'video/image_title_modify.html', context=context)


@login_required
def image_delete(request, image_id):
    try:
        image = Image.objects.get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404("Image does not exist")
    
    if request.method == 'POST':
        try:
            os.remove(image.image.path)
            image.delete()
        except:
            image.delete()

        messages.success(request, '图片删除成功！')
        return HttpResponseRedirect(reverse('video:media_list'))
    else:
        context = {'image': image}
        return render(request, 'video/image_delete.html', context=context)
    