# Generated by Django 3.2 on 2021-07-11 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0044_mcqanswersheet_question_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcqanswersheet',
            name='answer',
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name='tfanswersheet',
            name='answer',
            field=models.CharField(max_length=5),
        ),
    ]