# Generated by Django 2.2.4 on 2019-09-10 11:24

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20190910_1124'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='foodproduct',
            index=django.contrib.postgres.indexes.GinIndex(fields=['full_name'], name='food_foodpr_full_na_6029ee_gin'),
        ),
    ]