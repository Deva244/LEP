# Generated by Django 3.2 on 2021-05-14 00:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0015_alter_examsettings_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examsettings',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
