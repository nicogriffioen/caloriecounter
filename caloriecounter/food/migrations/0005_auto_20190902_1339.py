# Generated by Django 2.2.4 on 2019-09-02 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_auto_20190902_1245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['-is_base', '-is_constant', 'base_unit_multiplier']},
        ),
    ]