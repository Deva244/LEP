# Generated by Django 3.2 on 2021-07-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0040_mcqanswersheet_tfanswersheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcqanswersheet',
            name='answer',
            field=models.CharField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4)], max_length=1),
        ),
    ]
