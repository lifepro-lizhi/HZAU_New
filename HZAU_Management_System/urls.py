"""HZAU_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Basic import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', include('Basic.urls')),
    path('examination/', include('Examination.urls')),
    path('teacher/', include('Teacher.urls')),
    path('student/', include('Student.urls')),
    path('video/', include('Video.urls')),
    path('user_selection/', include('Basic.urls')),
    path('history/', include('History.urls')),
]

# admin.site.site_header = '华中农业大学 植物科学技术学院 后台管理系统'
admin.site.site_header = '黄冈师范学院 生物与农业资源学院 后台管理系统'

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
