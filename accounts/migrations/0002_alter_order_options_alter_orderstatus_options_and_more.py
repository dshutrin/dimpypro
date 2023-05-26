# Generated by Django 4.2.1 on 2023-05-20 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderstatus',
            options={'verbose_name': 'Статус задачи', 'verbose_name_plural': 'Статусы задач'},
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.FloatField(blank=True, verbose_name='Стоимость'),
        ),
    ]