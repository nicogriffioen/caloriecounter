# Generated by Django 2.2.4 on 2020-06-17 22:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0024_auto_20200608_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodproductunit',
            name='quantity',
            field=models.FloatField(default=1, help_text='The default quantity of this portion.', validators=[django.core.validators.MinValueValidator(1)], verbose_name='quantity'),
        ),
    ]