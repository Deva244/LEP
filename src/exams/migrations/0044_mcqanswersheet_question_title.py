# Generated by Django 3.2 on 2021-07-10 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0043_auto_20210711_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='mcqanswersheet',
            name='question_title',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='exams.exammcq'),
            preserve_default=False,
        ),
    ]
