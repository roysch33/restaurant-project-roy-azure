# Generated by Django 4.1.7 on 2023-06-03 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_delete_usernamemodel'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='cart',
            table='cart',
        ),
        migrations.AlterModelTable(
            name='delivery',
            table='delivery',
        ),
        migrations.AlterModelTable(
            name='item',
            table='item',
        ),
    ]
