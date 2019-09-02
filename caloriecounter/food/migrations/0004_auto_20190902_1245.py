# Generated by Django 2.2.4 on 2019-09-02 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_auto_20190902_1231'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='foodproduct',
            index=models.Index(fields=['full_name'], name='food_foodpr_full_na_8df215_idx'),
        ),
        migrations.AddIndex(
            model_name='foodproductnutrient',
            index=models.Index(fields=['product', 'nutrient'], name='food_foodpr_product_a04948_idx'),
        ),
    ]
