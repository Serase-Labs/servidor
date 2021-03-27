# Generated by Django 2.2.16 on 2021-03-27 18:33

import datetime
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Saldo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_ano', models.DateField()),
                ('saldo', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('cod_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PadraoMovimentacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receita_despesa', models.CharField(choices=[('receita', 'receita'), ('despesa', 'despesa'), ('divida', 'divida')], max_length=7)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('periodo', models.CharField(choices=[('semanal', 'semanal'), ('mensal', 'mensal'), ('anual', 'anual')], max_length=7)),
                ('valor', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('dia_cobranca', models.IntegerField()),
                ('data_geracao', models.DateField(blank=True, default=datetime.date.today)),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('cod_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serase_app.Categoria')),
                ('cod_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Movimentacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(blank=True, max_length=40, null=True)),
                ('valor_esperado', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('valor_pago', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('data_geracao', models.DateField(blank=True, null=True)),
                ('data_lancamento', models.DateField(blank=True, null=True)),
                ('cod_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serase_app.Categoria')),
                ('cod_padrao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='serase_app.PadraoMovimentacao')),
                ('cod_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Divida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credor', models.CharField(max_length=40)),
                ('valor_pago', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=9)),
                ('valor_divida', models.DecimalField(decimal_places=2, max_digits=9)),
                ('juros', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('juros_tipo', models.CharField(choices=[('composto', 'composto'), ('simples', 'simples'), ('não ativo', 'não ativo')], default='não ativo', max_length=8)),
                ('juros_ativos', models.BooleanField(default=False)),
                ('cod_padrao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serase_app.PadraoMovimentacao')),
            ],
        ),
    ]
