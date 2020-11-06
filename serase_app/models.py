from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Saldo(models.model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mes_ano = models.DateField()
    saldo = models.DecimalField(decimal_places=2)
    
class Movimentacao(models.model):
    data = models.DateField()
    valor_esperado = models.DecimalField(decimal_places=2)
    data_geracao = models.DateField()
    data_lancamento = models.DateField()
    valor_pago = models.DecimalField(decimal_places=2)
    usuario = cod_user=models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeingKey(Categoria, on_delete=models.CASCADE)

class Categoria(models.model):
    nome = models.CharField(max_length=20)
    
class PadraoMovimentacao(models.model):
    receita_despesa = models.BooleanField()
    descricao = models.TextField()
    periodo = models.IntegerField()
    valor = models.DecimalField(decimal_places=2)
    dia_cobranca = models.DateField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    usuario = cod_user=models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeingKey(Categoria, on_delete=models.CASCADE)