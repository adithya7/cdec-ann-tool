# Generated by Django 3.1.6 on 2021-04-05 01:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nlpviewer_backend', '0010_auto_20210404_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotationlog',
            name='endTime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 4, 21, 22, 15, 555106)),
        ),
        migrations.AlterField(
            model_name='annotationlog',
            name='startTime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 4, 21, 22, 15, 555029)),
        ),
    ]