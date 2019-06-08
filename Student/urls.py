from django.contrib import admin
from django.urls import path, include
from Student import views


app_name = 'student'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.student_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.student_logout, name='logout'),
    path('paper_list/<int:showEssayComment>', views.paper_list, name='paper_list'),
    path('video_list', views.video_list, name='video_list'),
    path('image_list', views.image_list, name='image_list'),
    path('paper_info/<int:paper_id>', views.paper_info, name='paper_info'),
    path('paper_results', views.paper_results, name='paper_results'),
    path('do_paper_type_choose/<int:paper_id>', views.do_paper_type_choose, name='do_paper_type_choose'),
    path('do_paper_multiple_choice/<int:paper_id>', views.do_paper_multiple_choice, name='do_paper_multiple_choice'),
    path('do_paper_essay/<int:paper_id>', views.do_paper_essay, name='do_paper_essay'),
    path('essay_comment_pick/<int:paper_id>', views.essay_comment_pick, name='essay_comment_pick'),
    path('pick_random_paper/<int:paper_id>', views.pick_random_paper, name='pick_random_paper'),
    path('do_comment/<int:paper_answer_id>', views.do_comment, name='do_comment'),
    path('completed_papers', views.completed_papers, name='completed_papers'),
    path('essay_comment_detail/<int:result_id>', views.essay_comment_detail, name='essay_comment_detail'),
    path('student_personal_info', views.student_personal_info, name='student_personal_info'),
    path('modify_personal_info', views.modify_personal_info, name='modify_personal_info'),
    path('reset_password', views.reset_password, name='reset_password'),
]