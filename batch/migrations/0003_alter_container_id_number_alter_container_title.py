# Generated by Django 4.2 on 2023-07-24 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0002_alter_batch_options_alter_pallet_is_placed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='id_number',
            field=models.CharField(max_length=255, unique=True, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='container',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Имя'),
        ),
    ]
