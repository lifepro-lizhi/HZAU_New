from django.contrib import admin
from django.urls import path, include
from Video import views


app_name = 'video'

urlpatterns = [
    path('upload_video', views.upload_video, name='upload_video'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('media_list', views.media_list, name='media_list'),
    path('video_play/<int:video_id>', views.video_play, name='video_play'),
    path('image_play/<int:image_id>', views.image_play, name='image_play'),
    path('video_manage/<int:video_id>', views.video_manage, name='video_manage'),
    path('image_manage/<int:image_id>', views.image_manage, name='image_manage'),
    path('video_title_modify/<int:video_id>', views.video_title_modify, name='video_title_modify'),
    path('video_delete/<int:video_id>', views.video_delete, name='video_delete'),
    path('image_title_modify/<int:image_id>', views.image_title_modify, name='image_title_modify'),
    path('image_delete/<int:image_id>', views.image_delete, name='image_delete'),
]