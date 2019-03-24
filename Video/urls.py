from django.contrib import admin
from django.urls import path, include
from Video import views


app_name = 'video'

urlpatterns = [
    path('upload_video', views.upload_video, name='upload_video'),
    path('video_list', views.video_list, name='video_list'),
    path('video_play/<int:video_id>', views.video_play, name='video_play'),
    path('video_manage/<int:video_id>', views.video_manage, name='video_manage'),
    path('video_title_modify/<int:video_id>', views.video_title_modify, name='video_title_modify'),
    path('video_delete/<int:video_id>', views.video_delete, name='video_delete'),
]