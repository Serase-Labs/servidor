# Arquivo para criação de códigos uteis para diversas views
from datetime import datetime
from .padroes_resposta import RespostaPaginacao

def converte_data_string(string):
    try:
        return datetime.strptime(string, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato incorreto para data, o formato esperado é YYYY-MM-DD")

def paginacao(request, lista):
    URL_PATH = request.path + "?"

    limite = int(request.GET["limite"])
    offset = int(request.GET["offset"]) if "offset" in request.GET else 0
    total = lista.count()

    limite_real = offset+limite if offset+limite<=total else total

    lista = lista[offset:limite_real]

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