# Generated by Django 2.2.4 on 2019-09-10 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0008_auto_20190910_0753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodproduct',
            name='display_name',
            field=models.TextField(null=True, verbose_name='display name'),
        ),
    ]
