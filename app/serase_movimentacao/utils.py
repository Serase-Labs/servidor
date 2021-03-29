# Arquivo para criação de códigos uteis para diversas views
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from serase_app.padroes_resposta import RespostaPaginacao, RespostaAtributoInvalido
from serase_app.models import *
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


def calcular_saldo(usuario, mes_ano=datetime.today(), hoje=datetime.today()):
    query_saldo = Saldo.objects.filter(cod_usuario=usuario)
    
    query_mes = query_saldo.filter(mes_ano__month=mes_ano.month, mes_ano__year=mes_ano.year)
    if query_mes.exists():
        saldo_mes = query_mes.first().saldo
    else:
        saldo_mes = 0.0

    query_saldo = query_saldo.filter(mes_ano__lte=mes_ano)
    saldo_total = query_saldo.aggregate(Sum("saldo"))["saldo__sum"] or 0

    return saldo_mes, saldo_total