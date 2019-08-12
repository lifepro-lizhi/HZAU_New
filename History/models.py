from django.db import models

# Create your models here.

class HistoryRecord(models.Model):
    name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=50)
    access_date = models.DateField(auto_now=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'history_record'
        verbose_name = '访问记录'
        verbose_name_plural = '访问记录'

