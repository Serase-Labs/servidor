# Generated by Django 3.1.5 on 2021-01-09 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serase_app', '0012_auto_20201119_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='padraomovimentacao',
            name='receita_despesa',
            field=models.CharField(choices=[('receita', 'receita'), ('despesa', 'despesa')], max_length=7),
        ),
    ]
