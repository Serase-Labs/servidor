# Generated by Django 3.1.3 on 2020-11-11 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serase_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movimentacao',
            name='data',
        ),
        migrations.AddField(
            model_name='movimentacao',
            name='descricao',
            field=models.CharField(default='nome empresa', max_length=40),
            preserve_default=False,
        ),
    ]
