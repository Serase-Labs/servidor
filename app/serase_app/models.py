from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

from datetime import datetime, date
from decimal import Decimal


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# Create your models here.
class Saldo(models.Model):
    cod_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mes_ano = models.DateField()
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return "["+str(self.mes_ano.month)+"/"+str(self.mes_ano.year)+"] - ("+str(self.saldo)+")" 

class Categoria(models.Model):
    nome = models.CharField(max_length=20)
    def __str__(self):
        return self.nome 

class PadraoMovimentacao(models.Model):
    TIPO_MOVIMENTACAO = (("receita","receita"),("despesa","despesa"),("divida","divida"))
    PERIODO_COBRANCA = (("semanal","semanal"),("mensal", "mensal"), ("anual","anual"))
    
    receita_despesa = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO)
    descricao = models.TextField(null=True, blank=True)
    periodo = models.CharField(max_length=7, choices=PERIODO_COBRANCA)
    valor = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    dia_cobranca = models.IntegerField() # mes=> dia util, semana=> dia da semana, ano=> mes
    data_geracao = models.DateField(default=date.today, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    cod_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cod_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    @property
    def ultima_cobranca(self):
        query = Movimentacao.objects.filter(cod_padrao=self)
        return query.latest("data_geracao") if query.exists() else None

    def __str__(self):
        return self.descricao 


class Movimentacao(models.Model):
    descricao = models.CharField(max_length=40, null=True, blank=True)
    valor_esperado = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    data_geracao = models.DateField(null=True, blank=True)
    data_lancamento = models.DateField(null=True, blank=True)
    cod_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cod_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    cod_padrao = models.ForeignKey(PadraoMovimentacao, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.descricao

class Divida(models.Model):

    TIPOS_DE_JUROS=(("composto","composto"),("simples","simples"), ("não ativo", "não ativo"))

    credor = models.CharField(max_length=40)
    valor_pago= models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    valor_divida= models.DecimalField(max_digits=9, decimal_places=2)
    juros= models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    juros_tipo=models.CharField(max_length=9, choices=TIPOS_DE_JUROS, default="não ativo")
    juros_ativos= models.BooleanField(default=False)
    cod_padrao = models.ForeignKey(PadraoMovimentacao, on_delete=models.CASCADE)


    def __str__(self):
        return self.credor 