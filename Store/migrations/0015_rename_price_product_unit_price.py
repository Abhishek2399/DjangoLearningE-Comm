# Generated by Django 4.1.1 on 2022-11-22 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0014_alter_orderitem_order_alter_orderitem_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='unit_price',
        ),
    ]
