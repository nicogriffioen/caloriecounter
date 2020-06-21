# Generated by Django 2.2.4 on 2020-05-31 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0017_auto_20200531_1006'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FoodProductSynonyms',
            new_name='FoodProductSynonym',
        ),
        migrations.RemoveIndex(
            model_name='foodproductsynonym',
            name='food_foodpr_text_d170aa_idx',
        ),
        migrations.AddIndex(
            model_name='foodproductsynonym',
            index=models.Index(fields=['text'], name='food_foodpr_text_a612ec_idx'),
        ),
    ]
