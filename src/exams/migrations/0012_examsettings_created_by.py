# Generated by Django 3.2 on 2021-05-14 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0011_alter_examsettings_exam_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='examsettings',
            name='created_by',
            field=models.CharField(default='manager', max_length=50),
            preserve_default=False,
        ),
    ]
