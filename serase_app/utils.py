# Arquivo para criação de códigos uteis para diversas views
from datetime import datetime

def converte_data_string(string):
    try:
        return datetime.strptime(string, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato incorreto para data, o formato esperado é YYYY-MM-DD")