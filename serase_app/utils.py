# Arquivo para criação de códigos uteis para diversas views
from datetime import datetime
from .padroes_resposta import RespostaPaginacao, RespostaAtributoInvalido
from .models import *
from django.db.models import F, Sum


# Funções de Data

def converte_data_string(string):
    """
        Retorna data convertida em objeto de data, ou erro caso formato esteja incorreto.
    """

    try:
        return datetime.strptime(string, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato incorreto para data, o formato esperado é YYYY-MM-DD")

def converte_mes_ano_string(string):
    """
        Retorna mês/ano convertido em objeto de data, ou erro caso formato esteja incorreto.
    """

    try:
        return datetime.strptime(string, '%Y-%m')
    except ValueError:
        raise ValueError("Formato incorreto para mês/ano, o formato esperado é YYYY-MM")

def mes_ano_atual():
    """
        Retorna a data correspondente ao mês/ano do dia atual.
    """

    return datetime.today()

def is_mes_ano_igual(mes_ano1, mes_ano2):
    """
        Retorna True se o mes e o ano das datas passadas forem iguais.
    """

    return mes_ano1.year==mes_ano2.year and mes_ano1.month==mes_ano2.month


# Outras

def paginacao(request, lista):
    """
        Trata parte de paginação de um queryset, retornando uma resposta de paginação ou de status caso um erro ocorra.
    """

    URL_PATH = request.path + "?"

    total = lista.count()

    # Pega atributo limite
    limite = int(request.GET["limite"])
    if limite <= 0:
        return RespostaAtributoInvalido("limite", limitacao="ser maior que zero")

    # Pega atributo offset caso exista
    offset = int(request.GET["offset"]) if "offset" in request.GET else 0
    if offset < 0:
        return RespostaAtributoInvalido("offset", limitacao="ser maior ou igual a zero")

    # Limita a pesquisa caso o limite estoure o maximo 
    limite_real = offset+limite if offset+limite<=total else total

    # Limita a lista
    lista = lista[offset:limite_real]

    # Define valores default das paginas como null
    proxima_pagina = None
    pagina_anterior = None

    # Gera link da proxima pagina
    if offset+limite<total:
        nova_query = request.GET.copy()
        nova_query["offset"] =  offset+limite
        proxima_pagina = URL_PATH+nova_query.urlencode()
    
    
    # Gera link da pagina atual
    if offset>0:
        novo_offset = 0 if offset - limite<0 else offset - limite
        nova_query = request.GET.copy()
        nova_query["offset"] = novo_offset
        pagina_anterior = URL_PATH+nova_query.urlencode()

    return RespostaPaginacao(200, list(lista), limite, total=total, offset=offset, proxima=proxima_pagina, anterior=pagina_anterior)


def calcular_saldo(usuario, mes_ano=mes_ano_atual(), hoje=mes_ano_atual()):
    saldo_mes = None
    saldo_total = None

    query_saldo = Saldo.objects.filter(cod_usuario=usuario)
    
    if is_mes_ano_igual(mes_ano, hoje):
        # Calcula saldo caso mês seja o mês atual, uma vez que não existe um objeto Saldo
        query_movimentacao = Movimentacao.objects.filter(cod_usuario=usuario, valor_pago__isnull=False)
        query_movimentacao = query_movimentacao.filter(data_lancamento__year=mes_ano.year, data_lancamento__month=mes_ano.month)
        saldo_mes = query_movimentacao.aggregate(Sum("valor_pago"))["valor_pago__sum"] or 0
    else:
        saldo = query_saldo.get(mes_ano__month=mes_ano.month, mes_ano__year=mes_ano.year)
        saldo_mes = saldo.saldo

    query_saldo = query_saldo.filter(mes_ano__lt=mes_ano.replace(day=1))
    saldo_total = query_saldo.aggregate(Sum("saldo"))["saldo__sum"] or 0
    saldo_total += saldo_mes

    return saldo_mes, saldo_total
