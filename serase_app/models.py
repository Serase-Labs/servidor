from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Saldo(models.Model):
    cod_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mes_ano = models.DateField()
    saldo = models.DecimalField(max_digits=10, decimal_places=2)

class Categoria(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome

class PadraoMovimentacao(models.Model):
    TIPO_MOVIMENTACAO = (("receita","receita"),("despesa","despesa"))
    
    receita_despesa = models.CharField(max_length=7, choices=TIPO_MOVIMENTACAO)
    descricao = models.TextField(null=True, blank=True)
    periodo = models.IntegerField()
    valor = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    dia_cobranca = models.IntegerField()
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    cod_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cod_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
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

