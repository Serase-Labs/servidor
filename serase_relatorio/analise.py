from .utils import *
from serase_app.models import *

from datetime import datetime, timedelta
from django.db.models import F, Sum, Q
from django.db.models.functions import Coalesce, Extract

def analise_resumo(usuario, periodo):
    data_inicio, data_fim = calcula_periodo(periodo)
    
    query = Movimentacao.objects.filter(cod_usuario=usuario, data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)

    receita = float(query.filter(valor_pago__gte=0).aggregate(Sum("valor_pago"))["valor_pago__sum"] or 0.0)
    despesa = float(query.filter(valor_pago__lt=0).aggregate(Sum("valor_pago"))["valor_pago__sum"] or 0.0)
    total = receita + despesa

    return {
        "gasto_total": despesa,
        "receita_total": receita,
        "fluxo_total": total 
    }

def analise_categoria(usuario, periodo):
    data_inicio, data_fim = calcula_periodo(periodo)
    data_inicio_passado, data_fim_passado = calcula_periodo_anterior(periodo)

    categoria_ids = []

    # Seleciona despesas do usuario
    query = Movimentacao.objects.filter(cod_usuario=usuario, valor_pago__lt=0) 
    # Agrupa despesas por categoria
    query = query.values('cod_categoria')


    # 1- Calcular maior despesa

    # Seleciona despesas do periodo atual
    qperiodo_atual = query.filter(data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)
    # Soma todas as despesas de uma categoria em 'despesa_total' e ordena em ordem decrescente de despesa (maior despesa na frente)
    qperiodo_atual = qperiodo_atual.annotate(despesa_total=Sum('valor_pago')).order_by("despesa_total")

    if qperiodo_atual.count() > 0:
        cod_categ_despesa = qperiodo_atual.first()['cod_categoria']
        categoria_ids.append(cod_categ_despesa)
    else:
        cod_categ_despesa = None


    # 2 - Calcular maior salto/economia

    # Seleciona despesas entre o começo do ultimo periodo e o final do periodo atual
    qrelacao_ultimo = query.filter(data_lancamento__gte=data_inicio_passado, data_lancamento__lte=data_fim)
    
    # Cria atributo 'despesa_total', composta da soma das despesas do periodo atual menos a soma das despesas do ultimo periodo
    # Assim, 'despesa_total' é o valor a mais gasto em relação ao periodo passado. 
    # Ex: despesa_total: -700, significa que foi gasto +700 reais em relação ao mês passado
    #     despesa_total: +50, significa que foi gasto -50 reais em relação ao mês passado
    # Os sinais são invertidos pelo fato de uma movimentação de despesa possuir valores negativos.  
    qrelacao_ultimo = qrelacao_ultimo.annotate(
        despesa_total= Coalesce(Sum('valor_pago', filter=Q(data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)), 0.0) 
        - Coalesce(Sum('valor_pago', filter=Q(data_lancamento__gte=data_inicio_passado, data_lancamento__lte=data_fim_passado)),0.0)
    )

    # Ao ordernar temos no topo da lista o maior salto e no fim a maior economia
    qrelacao_ultimo = qrelacao_ultimo.order_by('despesa_total')

    if qrelacao_ultimo.count() > 0:
        cod_categ_salto = qrelacao_ultimo.first()['cod_categoria']
        cod_categ_economia = qrelacao_ultimo.last()['cod_categoria']
        categoria_ids.append(cod_categ_salto)
        categoria_ids.append(cod_categ_economia)
    else:
        cod_categ_salto = None
        cod_categ_economia = None

    
    # Pegar os nomes de cada categoria através de seus ids
    categorias = Categoria.objects.filter(id__in=categoria_ids)
    if qperiodo_atual.count() > 0:
        cod_categ_economia = categorias.get(id=cod_categ_economia).nome
    
    if qrelacao_ultimo.count() > 0:
        cod_categ_salto = categorias.get(id=cod_categ_salto).nome
        cod_categ_despesa = categorias.get(id=cod_categ_despesa).nome

    return {
        "maior_despesa": cod_categ_despesa,
        "maior_salto": cod_categ_salto,
        "maior_economia": cod_categ_economia,
    }

def grafico_semanal(usuario):
    data_inicio, data_fim = calcula_periodo("semana")

    query = Movimentacao.objects.filter(cod_usuario=usuario, data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)
    query = query.annotate(dia=Extract("data_lancamento", "week_day")).values("dia")
    query = query.annotate(
        receita=Coalesce(Sum('valor_pago', filter=Q(valor_pago__gte=0)), 0.0),
        despesa=Coalesce(Sum('valor_pago', filter=Q(valor_pago__lt=0)), 0.0)
    ).values("dia","receita","despesa").order_by("dia")

    lista_dias_inclusos = list(query.values_list("dia", flat=True))
    resultado = list(query)

    for obj in resultado:
        obj['receita'] = round(obj['receita'], 2)
        obj['despesa'] = round(obj['despesa'], 2)

    for i in list(set(range(1,8)) - set(lista_dias_inclusos)):
        receita = 0.0
        despesa = 0.0
        resultado.append({"dia": i, "receita": receita, "despesa": despesa})

    return sorted(resultado, key=lambda k: k['dia'])
