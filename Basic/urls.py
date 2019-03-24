from django.contrib import admin
from django.urls import path, include
from Basic import views


app_name = 'basic'

urlpatterns = [
    path('', views.index, name='index'),
]