from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Saldo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mes_ano = models.DateField()
    saldo = models.DecimalField(max_digits=10 ,decimal_places=2)

class Categoria(models.Model):
    nome = models.CharField(max_length=20)

class Movimentacao(models.Model):
    
    valor_esperado = models.DecimalField(max_digits=6 ,decimal_places=2)
    data_geracao = models.DateField()
    data_lancamento = models.DateField()
    valor_pago = models.DecimalField(max_digits=9 ,decimal_places=2)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    descricao= models.CharField(max_length=40)
class PadraoMovimentacao(models.Model):
    receita_despesa = models.BooleanField()
    descricao = models.TextField()
    periodo = models.IntegerField()
    valor = models.DecimalField(max_digits=6 ,decimal_places=2)
    dia_cobranca = models.DateField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)