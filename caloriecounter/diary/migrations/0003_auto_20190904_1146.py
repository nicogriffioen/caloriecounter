# Generated by Django 2.2.4 on 2019-09-04 11:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0002_auto_20190902_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='diaryentry',
            name='date',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Entry Date'),
        ),
        migrations.AddField(
            model_name='diaryentry',
            name='time',
            field=models.TimeField(default=datetime.datetime.now, verbose_name='Entry Time'),
        ),
        migrations.AlterField(
            model_name='diaryentry',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
