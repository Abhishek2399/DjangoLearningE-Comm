# Generated by Django 4.1.1 on 2022-11-22 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0016_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='-'),
        ),
    ]
