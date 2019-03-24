from django.contrib import admin
from django.urls import path, include
from Student import views


app_name = 'student'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.student_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.student_logout, name='logout'),
    path('paper_list', views.paper_list, name='paper_list'),
    path('video_list', views.video_list, name='video_list'),
    path('paper_info/<int:paper_id>', views.paper_info, name='paper_info'),
    path('paper_results', views.paper_results, name='paper_results'),
    path('do_paper_type_choose/<int:paper_id>', views.do_paper_type_choose, name='do_paper_type_choose'),
    path('do_paper_multiple_choice/<int:paper_id>', views.do_paper_multiple_choice, name='do_paper_multiple_choice'),
    path('do_paper_essay/<int:paper_id>', views.do_paper_essay, name='do_paper_essay'),
]