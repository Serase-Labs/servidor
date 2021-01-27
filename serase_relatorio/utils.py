from datetime import datetime, timedelta

def calcula_periodo(periodo, hoje=datetime.today()):
    """
        periodo: semana, mes, ano;
    """
    if periodo=="semana":
        comeco = hoje - timedelta(days=hoje.weekday()+1)
        fim = comeco + timedelta(days=6)
    elif periodo=="mes":
        comeco = hoje.replace(day=1)
        prox_mes = hoje.replace(day=28) + timedelta(days=4)
        fim = prox_mes - timedelta(days=prox_mes.day)
    elif periodo=="ano":
        comeco = hoje.replace(month=1, day=1)
        fim = hoje.replace(month=12, day=31)
    else:
        return None,None

    return comeco, fim

def calcula_periodo_anterior(periodo, hoje=datetime.today()):
    if periodo=="semana":
        data = hoje - timedelta(days=7)
    elif periodo=="mes":
        mes = hoje.replace(day=1) - timedelta(days=1)
        data = hoje.replace(month=mes.month, year=mes.year)
    elif periodo=="ano":
        data = hoje - timedelta(years=1)
    else:
        return None, None

    return calcula_periodo(periodo,data)