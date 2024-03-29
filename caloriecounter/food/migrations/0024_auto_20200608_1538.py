# Generated by Django 2.2.4 on 2020-06-08 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0023_auto_20200608_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.TextField(blank=True, help_text='i.e. gram', null=True, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='short_name',
            field=models.TextField(blank=True, help_text='i.e. g', null=True, verbose_name='Short name'),
        ),
    ]
