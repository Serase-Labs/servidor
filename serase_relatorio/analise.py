from .utils import calcula_periodo
from serase_app.models import *

from django.db.models import F, Sum

def analise_resumo(periodo):
    usuario = User.objects.get(username="jv_eumsmo")
    
    data_inicio, data_fim = calcula_periodo(periodo)
    
    query = Movimentacao.objects.filter(data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)

    receita = float(query.filter(valor_pago__gte=0).aggregate(Sum("valor_pago"))["valor_pago__sum"] or 0.0)
    despesa = float(query.filter(valor_pago__lt=0).aggregate(Sum("valor_pago"))["valor_pago__sum"] or 0.0)
    total = receita + despesa

    return {
        "gasto_total": despesa,
        "receita_total": receita,
        "fluxo_total": total 
    }