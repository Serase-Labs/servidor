from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db.models.signals import pre_delete

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

    def save(self,*args,**kwargs):
        """
        Chamada no ato de salvar uma instancia no BD.
        Compara valores anteriores de valor e data e altera o saldo.
        """

        # Modificando o Saldo automaticamente apartir de uma movimentação

        old = Movimentacao.objects.filter(pk=getattr(self,"pk",None)).first()

        # Se havia informações prévias sobre a movimentação (ou seja, se for uma alteração)
        if old:
            # Se houve alteração na data da movimentação
            if old.data_lancamento!=self.data_lancamento:
                new_date = datetime(year=self.data_lancamento.year, month=self.data_lancamento.month, day=1)
                saldo_old = Saldo.objects.get(cod_usuario=self.cod_usuario,mes_ano__month=old.data_lancamento.month, mes_ano__year=old.data_lancamento.year)
                saldo_new, c = Saldo.objects.get_or_create(cod_usuario=self.cod_usuario,mes_ano=new_date)
                
                # Se os meses do saldo não são o mesmo na alteração de movimentação
                if saldo_old.mes_ano != saldo_new.mes_ano:
                    # Remove saldo do mês da data anterior e adiciona no mês da nova data
                    saldo_old.saldo -= old.valor_pago
                    saldo_new.saldo += self.valor_pago
                    Saldo.objects.bulk_update([saldo_old, saldo_new], ["saldo"])
                else:
                    # Subtrai diferença com saldo anterior
                    saldo_new.saldo += self.valor_pago - old.valor_pago
                    saldo_new.save()

            # Houve alteração no valor e não na data
            elif old.valor_pago!=self.valor_pago:
                # Subtrai diferença com saldo anterior
                saldo = Saldo.objects.get(cod_usuario=self.cod_usuario,mes_ano__month=self.data_lancamento.month, mes_ano__year=self.data_lancamento.year)
                saldo.saldo += self.valor_pago - old.valor_pago
                saldo.save()
        else:
            mes_ano = datetime.strptime(self.data_lancamento, '%Y-%m-%d')
            mes_ano = mes_ano.replace(day=1)
            saldo, c = Saldo.objects.get_or_create(cod_usuario=self.cod_usuario, mes_ano=mes_ano)
            saldo.saldo+=Decimal(self.valor_pago)
            saldo.save()

        super(Movimentacao,self).save(*args,**kwargs)
    
    @staticmethod
    def pre_delete(sender, **kwargs):
        """ 
        Chamada antes de uma movimentação ser deletada.
        Subtrai seu valor no objeto saldo.
        """
        
        instance = kwargs.get('instance')
        if instance.data_lancamento != None:
            epoca = instance.data_lancamento
            saldo = Saldo.objects.get(cod_usuario=instance.cod_usuario,mes_ano__month=epoca.month, mes_ano__year=epoca.year)
            saldo.saldo -= instance.valor_pago
            saldo.save()

    def __str__(self):
        return self.descricao

pre_delete.connect(Movimentacao.pre_delete, sender=Movimentacao)

class Divida(models.Model):

    TIPOS_DE_JUROS=(("composto","composto"),("simples","simples"), ("não ativo", "não ativo"))

    credor = models.CharField(max_length=40)
    valor_pago= models.DecimalField(max_digits=9, decimal_places=2, default=Decimal('0.00'))
    valor_divida= models.DecimalField(max_digits=9, decimal_places=2)
    juros= models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    juros_tipo=models.CharField(max_length=8, choices=TIPOS_DE_JUROS, default="não ativo")
    juros_ativos= models.BooleanField(default=False)
    cod_padrao = models.ForeignKey(PadraoMovimentacao, on_delete=models.CASCADE)


    def __str__(self):
        return self.credor 