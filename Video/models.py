from django.db import models
from Teacher.models import Teacher
from pypinyin import lazy_pinyin

# Create your models here.

def user_directory_path(instance, filename):
    pinyin_list = lazy_pinyin(instance.teacher.name)
    name_pinyin = ""
    for item in pinyin_list[:-1]:
        name_pinyin += item + '_'
    name_pinyin += pinyin_list[-1]

    return '{0}/{1}'.format(name_pinyin, filename)


class Video(models.Model):
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now=True)
    video = models.FileField(upload_to=user_directory_path)

    class Meta:
        db_table = 'video'
        verbose_name = '媒体库(视频)'
        verbose_name_plural = '媒体库(视频)'


class Image(models.Model):
    title = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now=True)
    image = models.ImageField(upload_to=user_directory_path)

    class Meta:
        db_table = 'image'
        verbose_name = '媒体库(图片)'
        verbose_name_plural = '媒体库(图片)'

