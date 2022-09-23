# Generated by Django 3.2 on 2021-07-07 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0034_auto_20210707_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exammcq',
            name='correct_answer',
            field=models.CharField(choices=[(1, 1), (2, 2), (3, 3), (4, 4)], max_length=1),
        ),
        migrations.AlterField(
            model_name='examtf',
            name='correct_answer',
            field=models.CharField(choices=[(True, True), (False, False)], max_length=5),
        ),
    ]