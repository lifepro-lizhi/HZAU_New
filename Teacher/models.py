from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)

    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'teacher'
        verbose_name = '教师'
        verbose_name_plural = '教师'
    
