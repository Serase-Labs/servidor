# Arquivo para criação de códigos uteis para diversas views
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
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
    query_saldo = Saldo.objects.filter(cod_usuario=usuario)
    
    query_mes = query_saldo.filter(mes_ano__month=mes_ano.month, mes_ano__year=mes_ano.year)
    if query_mes.exists():
        saldo_mes = query_mes.first().saldo
    else:
        saldo_mes = 0.0

    query_saldo = query_saldo.filter(mes_ano__lte=mes_ano)
    saldo_total = query_saldo.aggregate(Sum("saldo"))["saldo__sum"] or 0

    return saldo_mes, saldo_total

# Funções relativas a cobrança

def add_business_days(from_date, number_of_days):
    to_date = from_date
    while number_of_days:
       to_date += timedelta(1)
       if to_date.weekday() < 5: # i.e. is not saturday or sunday
           number_of_days -= 1
    return to_date

def week_num(date):
    return date.isocalendar()[1]

def correct_weekday(date):
    # Data começando no domingo como 0
    return date.isoweekday()%7

def business_days_in_month(mes, dias):
    data = mes.replace(day=1) - timedelta(days=1)
    return add_business_days(data, dias)

def day_of_week(semana,day):
    # 1=domingo, 2=segunda, ..., 7=sabado
    data = semana + timedelta(days=correct_weekday(semana)-1 + day)
    return data

def month_of_year(ano, mes):
    data = ano.replace(day=1,month=mes)
    return data
