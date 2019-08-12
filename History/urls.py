from django.contrib import admin
from django.urls import path, include
from History import views


app_name = 'history'

urlpatterns = [
    path('list_records', views.list_records, name='list_records'),
    path('recent_records_detail', views.recent_records_detail, name='recent_records_detail'),
]