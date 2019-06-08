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
    path('export_paper_results/<int:paper_id>', views.export_paper_results, name='export_paper_results'),
    path('export_paper_to_pdf/<int:paper_id>', views.export_paper_to_pdf, name='export_paper_to_pdf'),
    path('teacher_personal_info', views.teacher_personal_info, name='teacher_personal_info'),
    path('modify_personal_info', views.modify_personal_info, name='modify_personal_info'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('grade_class_list', views.grade_class_list, name='grade_class_list'),
    path('grade_class_detail/<int:gradeclass_id>', views.grade_class_detail, name='grade_class_detail'),
    path('export_grade_class_detail/<int:gradeclass_id>', views.export_grade_class_detail, name='export_grade_class_detail'),
]