from django.contrib import admin
from django.urls import path, include
from Basic import views


app_name = 'basic'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.user_selection, name='user_selection'),
    path('login', views.user_login, name='user_login'),
    path('guest_login', views.guest_login, name='guest_login'),
    path('guest_name', views.guest_name, name='guest_name'),
    path('start', views.start, name='start'),
]