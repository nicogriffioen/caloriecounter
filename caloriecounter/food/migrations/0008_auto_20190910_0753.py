# Generated by Django 2.2.4 on 2019-09-10 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0007_auto_20190909_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodproduct',
            name='display_name',
            field=models.TextField(blank=True, null=True, verbose_name='display name'),
        ),
    ]
