from datetime import datetime, timedelta
from serase_app.padroes_resposta import RespostaAtributoInvalido

def get_hoje():
    return datetime.strptime("2020-09-10", '%Y-%m-%d')#datetime.today()

def calcula_periodo(periodo, hoje=get_hoje()):
    """
        periodo: semana, mes, ano;
    """
    if periodo=="semanal":
        comeco = hoje - timedelta(days=hoje.weekday()+1)
        fim = comeco + timedelta(days=6)
    elif periodo=="mensal":
        comeco = hoje.replace(day=1)
        prox_mes = hoje.replace(day=28) + timedelta(days=4)
        fim = prox_mes - timedelta(days=prox_mes.day)
    elif periodo=="anual":
        comeco = hoje.replace(month=1, day=1)
        fim = hoje.replace(month=12, day=31)
    else:
        return None,None

    return comeco, fim

def calcula_periodo_anterior(periodo, hoje=get_hoje()):
    if periodo=="semanal":
        data = hoje - timedelta(days=7)
    elif periodo=="mensal":
        mes = hoje.replace(day=1) - timedelta(days=1)
        data = hoje.replace(month=mes.month, year=mes.year)
    elif periodo=="anual":
        data = hoje.replace(year=hoje.year-1)
    else:
        return None, None

    return calcula_periodo(periodo,data)


PERIODOS_VALIDOS = ["semanal", "mensal", "anual"]

def validade_periodo(periodo):
    if periodo not in PERIODOS_VALIDOS:
        return False
    return True

def erro_periodo(periodo):
    return RespostaAtributoInvalido("periodo", periodo, PERIODOS_VALIDOS)