# Generated by Django 4.2.1 on 2023-05-22 10:51

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_order_created_at_alter_customuser_avatar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='end_of',
            field=models.DateField(default=accounts.utils.get_sale_end_date, verbose_name='Действует до'),
        ),
    ]
