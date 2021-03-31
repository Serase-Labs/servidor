from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save

from .models import *

@receiver(pre_delete, sender=Movimentacao)
def pre_delete_movimentacao(sender, **kwargs):
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


@receiver(pre_save, sender=Movimentacao)
def pre_save_movimentacao(sender, **kwargs):
    """
    Chamada no ato de salvar uma instancia no BD.
    Compara valores anteriores de valor e data e altera o saldo.
    """

    instance = kwargs.get('instance')

    # Modificando o Saldo automaticamente apartir de uma movimentação
    old = Movimentacao.objects.filter(id=instance.id).first()

    if instance.cod_padrao and instance.cod_padrao.receita_despesa=="divida" and instance.valor_pago:
        divida = Divida.objects.get(cod_padrao=instance.cod_padrao)

        diferenca = (instance.valor_pago or 0) - ((old.valor_pago or 0) if old else 0)
        divida.valor_pago -= diferenca
        divida.save()



    # Se havia informações prévias sobre a movimentação (ou seja, se for uma alteração)
    if old:
        # Se houve alteração na data da movimentação
        if old.data_lancamento!=instance.data_lancamento and old.data_lancamento:
            new_date = instance.data_lancamento.replace(day=1)
            old_date = old.data_lancamento.replace(day=1)
            saldo_old, d = Saldo.objects.get_or_create(cod_usuario=instance.cod_usuario,mes_ano=old_date)
            saldo_new, c = Saldo.objects.get_or_create(cod_usuario=instance.cod_usuario,mes_ano=new_date)
            
            # Se os meses do saldo não são o mesmo na alteração de movimentação
            if saldo_old.mes_ano != saldo_new.mes_ano:
                # Remove saldo do mês da data anterior e adiciona no mês da nova data
                saldo_old.saldo -= old.valor_pago
                saldo_new.saldo += instance.valor_pago
                Saldo.objects.bulk_update([saldo_old, saldo_new], ["saldo"])
            else:
                # Subtrai diferença com saldo anterior
                saldo_new.saldo += instance.valor_pago - old.valor_pago
                saldo_new.save()
        # Houve alteração no valor e não na data
        elif old.valor_pago!=instance.valor_pago:
            # Subtrai diferença com saldo anterior
            mes_ano = instance.data_lancamento.replace(day=1)
            saldo, c = Saldo.objects.get_or_create(cod_usuario=instance.cod_usuario,mes_ano=mes_ano)
            saldo.saldo += instance.valor_pago - (old.valor_pago or 0)
            saldo.save()
    else:
        if instance.data_lancamento:
            mes_ano = instance.data_lancamento
            mes_ano = mes_ano.replace(day=1)
            saldo, c = Saldo.objects.get_or_create(cod_usuario=instance.cod_usuario, mes_ano=mes_ano)
            saldo.saldo+=Decimal(instance.valor_pago)
            saldo.save()

