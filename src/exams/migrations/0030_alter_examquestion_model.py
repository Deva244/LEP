# Generated by Django 3.2 on 2021-05-19 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0029_auto_20210519_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examquestion',
            name='model',
            field=models.IntegerField(default=0),
        ),
    ]