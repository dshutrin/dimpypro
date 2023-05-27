# Generated by Django 4.2.1 on 2023-05-27 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_order_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='promo',
        ),
        migrations.AddField(
            model_name='order',
            name='need_payment_system',
            field=models.BooleanField(default=False, verbose_name='Требуется платёжная система'),
        ),
    ]