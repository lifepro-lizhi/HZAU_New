# Generated by Django 2.1.5 on 2019-02-28 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0004_auto_20190224_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperresult',
            name='choice_question_result',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='paperresult',
            name='essay_question_result',
            field=models.IntegerField(default=0),
        ),
    ]
