# Generated by Django 3.2 on 2021-05-16 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0024_auto_20210516_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examquestion',
            name='choice1',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='examquestion',
            name='choice2',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='examquestion',
            name='choice3',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='examquestion',
            name='choice4',
            field=models.CharField(max_length=50),
        ),
    ]