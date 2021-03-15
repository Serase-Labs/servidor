# Generated by Django 2.2.16 on 2021-03-12 18:46

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serase_app', '0014_auto_20210122_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saldo',
            name='saldo',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]