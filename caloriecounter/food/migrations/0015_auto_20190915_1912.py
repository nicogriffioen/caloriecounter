# Generated by Django 2.2.4 on 2019-09-15 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0014_auto_20190915_1900'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FoodProductSearchCache',
            new_name='FoodProductSearchCacheItem',
        ),
    ]