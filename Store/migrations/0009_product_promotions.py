# Generated by Django 4.1.1 on 2022-11-18 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0008_rename_cutomer_address_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='promotions',
            field=models.ManyToManyField(to='Store.promotion'),
        ),
    ]