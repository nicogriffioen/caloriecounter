# Generated by Django 2.2.4 on 2019-09-10 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voice', '0002_auto_20190910_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voicesessionitem',
            name='type',
            field=models.CharField(choices=[('user_input', 'User input'), ('feedback', 'Voice assistant feedback'), ('clarification_question', 'Voice assistant clarification question'), ('objects_created', 'Object created')], max_length=255, verbose_name='type of chat item'),
        ),
    ]
