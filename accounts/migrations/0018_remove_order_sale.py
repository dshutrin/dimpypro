# Generated by Django 4.2.1 on 2023-05-27 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_alter_order_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sale',
        ),
    ]
