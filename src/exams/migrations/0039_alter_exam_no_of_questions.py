# Generated by Django 3.2 on 2021-07-07 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0038_exam_no_of_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='no_of_questions',
            field=models.IntegerField(default=0),
        ),
    ]