# Generated by Django 4.1.1 on 2022-11-17 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_alter_customer_table'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['first_name', 'last_name'], name='store_custo_first_n_a7e990_idx'),
        ),
    ]
