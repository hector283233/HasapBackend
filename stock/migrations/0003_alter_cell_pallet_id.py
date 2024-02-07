# Generated by Django 4.2 on 2023-06-16 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0002_alter_batch_options_alter_pallet_is_placed'),
        ('stock', '0002_cell_pallet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='pallet_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cell_pallet', to='batch.pallet', verbose_name='Паллет'),
        ),
    ]
