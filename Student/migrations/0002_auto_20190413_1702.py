# Generated by Django 2.1.5 on 2019-04-13 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essaycomment',
            name='score',
            field=models.FloatField(default=0, null=True),
        ),
    ]