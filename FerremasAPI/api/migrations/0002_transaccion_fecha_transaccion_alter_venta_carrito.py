# Generated by Django 4.2.1 on 2024-04-30 21:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='fecha_transaccion',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='venta',
            name='carrito',
            field=models.BooleanField(verbose_name='False para venta y True para carrito'),
        ),
    ]