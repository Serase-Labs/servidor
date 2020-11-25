# Arquivo para criação de códigos uteis para diversas views
from datetime import datetime
from .padroes_resposta import RespostaPaginacao, RespostaAtributoInvalido

def converte_data_string(string):
    """
        Retorna data convertida em objeto de data, ou erro caso formato esteja incorreto
    """

    try:
        return datetime.strptime(string, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Formato incorreto para data, o formato esperado é YYYY-MM-DD")

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