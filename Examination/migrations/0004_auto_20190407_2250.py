# Generated by Django 2.1.5 on 2019-04-07 14:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Examination', '0003_auto_20190405_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='expire_date',
            field=models.DateField(default=datetime.date(2019, 5, 7)),
        ),
    ]
