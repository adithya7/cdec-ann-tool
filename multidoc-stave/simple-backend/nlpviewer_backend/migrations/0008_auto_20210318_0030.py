# Generated by Django 3.1.6 on 2021-03-18 04:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nlpviewer_backend', '0007_auto_20210317_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotationlog',
            name='endTime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 18, 0, 30, 30, 41052)),
        ),
        migrations.AlterField(
            model_name='annotationlog',
            name='startTime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 18, 0, 30, 30, 40997)),
        ),
    ]
