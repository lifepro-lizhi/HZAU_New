from django.contrib import admin
from django.urls import path
from Examination import views


app_name = 'examination'

urlpatterns = [
    path("create_paper", views.create_paper, name="create_paper"),
    path("<int:paper_id>/choose_create_type", views.choose_create_type, name="choose_create_type"),
    path("<int:paper_id>/create_multiple_choice_question/", views.create_multiple_choice_question, name="create_multiple_choice_question"),
    path("<int:paper_id>/create_essay_question", views.create_essay_question, name="create_essay_question"),
    path("paper_list", views.paper_list, name="paper_list"),
    path("<int:paper_id>", views.paper_detail, name="paper_detail"),
    path("modify_multiple_choice_question/<int:question_id>", views.modify_multiple_choice_question, name="modify_multiple_choice_question"),
    path("modify_essay_question/<int:question_id>", views.modify_essay_question, name="modify_essay_question"),
    path("delete_multiple_choice_question/<int:question_id>", views.delete_multiple_choice_question, name="delete_multiple_choice_question"),
    path("delete_essay_question/<int:question_id>", views.delete_essay_question, name="delete_essay_question"),
    path("modify_paper/<int:paper_id>", views.modify_paper, name="modify_paper"),
    path("publish_paper/<int:paper_id>", views.publish_paper, name="publish_paper"),
    path("delete_paper/<int:paper_id>", views.delete_paper, name="delete_paper"),
    path("paper_info/<int:paper_id>", views.paper_info, name="paper_info"),
    path("paper_preview/<int:paper_id>", views.paper_preview, name="paper_preview"),
    path("paper_results/<int:paper_id>", views.paper_results, name="paper_results"),
]