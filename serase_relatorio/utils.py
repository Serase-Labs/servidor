from datetime import datetime, timedelta

def calcula_periodo(periodo):
    """
        periodo: semana, mes, ano;
    """
    hoje = datetime.today()

    if periodo=="semana":
        comeco = hoje - timedelta(days=hoje.weekday())
        fim = hoje + timedelta(days=6)
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