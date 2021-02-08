from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from decimal import Decimal

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

    def save(self,*args,**kwargs):
        old = Movimentacao.objects.filter(pk=getattr(self,"pk",None)).first()
        if old:
            if old.data_lancamento!=self.data_lancamento:
                new_date = datetime(year=self.data_lancamento.year, month=self.data_lancamento.month, day=1)
                saldo_old = Saldo.objects.get(cod_usuario=self.cod_usuario,mes_ano__month=old.data_lancamento.month, mes_ano__year=old.data_lancamento.year)
                saldo_new, c = Saldo.objects.get_or_create(cod_usuario=self.cod_usuario,mes_ano=new_date)
                saldo_old.saldo-=old.valor_pago
                saldo_new.saldo+=self.valor_pago
                
                Saldo.objects.bulk_update([saldo_old, saldo_new], ["saldo"])
            elif old.valor_pago!=self.valor_pago:
                diferenca = self.valor_pago - old.valor_pago
                saldo = Saldo.objects.get(cod_usuario=self.cod_usuario,mes_ano__month=self.data_lancamento.month, mes_ano__year=self.data_lancamento.year)
                saldo.saldo+=diferenca
                saldo.save()
        else:
            mes_ano = datetime.strptime(self.data_lancamento, '%Y-%m-%d')
            mes_ano = mes_ano.replace(day=1)
            saldo, c = Saldo.objects.get_or_create(cod_usuario=self.cod_usuario, mes_ano=mes_ano)
            saldo.saldo+=Decimal(self.valor_pago)
            saldo.save()

        super(Movimentacao,self).save(*args,**kwargs)

    def __str__(self):
        return self.descricao 

class Divida(models.Model):

    TIPOS_DE_JUROS=(("composto","composto"),("simples","simples"))

    credor = models.CharField(max_length=40, null=True, blank=True)
    valor_pago= models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    valor_divida= models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    juros= models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    juros_tipo=models.CharField(max_length=8, choices=TIPOS_DE_JUROS)
    juros_ativos= models.BooleanField(default=False)
    cod_padrao = models.ForeignKey(PadraoMovimentacao, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.credor 