# Generated by Django 4.1.6 on 2023-02-11 16:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "Store",
            "0019_rename_store_custo_first_n_a7e990_idx_store_custo_first_n_8f83e0_idx_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collection",
            options={"ordering": ["title"]},
        ),
        migrations.AlterField(
            model_name="product",
            name="inventory",
            field=models.IntegerField(
                validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="unit_price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=6,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
    ]