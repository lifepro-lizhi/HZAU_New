# Generated by Django 2.1.5 on 2019-02-24 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0002_auto_20190224_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperresult',
            name='choice_question_result',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='paperresult',
            name='essay_question_result',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='paperresult',
            name='submit_date',
            field=models.DateField(auto_now=True),
        ),
    ]
