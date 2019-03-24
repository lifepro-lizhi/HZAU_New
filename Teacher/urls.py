from django.contrib import admin
from django.urls import path, include
from Teacher import views


app_name = 'teacher'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.teacher_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.teacher_logout, name='logout'),
    path('papers', views.teacher_papers, name='papers'),
    path('uploaded_videos', views.uploaded_videos, name='uploaded_videos'),
    path('paper_results_list', views.paper_results_list, name='paper_results_list'),
]