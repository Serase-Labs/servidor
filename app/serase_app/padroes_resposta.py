from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework import serializers

# Padrões de Respostas

def Resposta(status, conteudo):
    return JsonResponse(conteudo, status=status, json_dumps_params={'indent': 2, 'ensure_ascii':False})

def RespostaStatus(status,mensagem:str):
    return Resposta(status, {"status": status, "mensagem": mensagem})

def RespostaErroDetalhado(status, erros:list):
    mensagem = "Problema no atributo '"+erros[0]["campo"]+"': "+erros[0]["erro"] if len(erros) > 0 else "Eita! Algo está errado :("
    return Resposta(status, {"status": status, "mensagem": mensagem, "erros": erros})

def RespostaConteudo(status, conteudo):
    return Resposta(status, {"status": status, "conteudo": conteudo})

def RespostaLista(status, conteudo, total=None):
    total = total if total else len(conteudo)
    return Resposta(status, {"status": status, "conteudo": conteudo, "total": total})

def RespostaPaginacao(status, conteudo, limite, total=None, offset=0, proxima=None, anterior=None):
    total = total if total else len(conteudo)
    return Resposta(status, {"status": status, "conteudo": conteudo, "total": total, "limite": limite, "offset": offset, "proxima": proxima, "anterior": anterior})


# Respostas Padrões

def RespostaNotFound():
    return RespostaStatus(404, "Página não encontrada!")

def RespostaAtributoInvalido(atributo, valor=None, escolhas=None, limitacao=None):
    mensagem = f"Atributo '{atributo}' não aceita o valor "
    
    if valor:
        mensagem += f"'{valor}'"
    else:
        mensagem += "inserido" 
    
    if escolhas:
        mensagem += ". Os valores aceitos são: "
        mensagem += ", ".join(escolhas)
        mensagem += "."
    elif limitacao:
        mensagem += ". O valor deve "
        mensagem += limitacao
        mensagem += "."
    else:
        mensagem += "!"

    
    return RespostaStatus(400, mensagem)
    
def RespostaFormatoDataInvalido():
    return RespostaStatus(400, "Formato incorreto para data, o formato esperado é YYYY-MM-DD")


def listaErrosValidacao(erros):
    lista = list()
    for campo in erros:
        if campo=="status":
            continue
        
        if isinstance(erros[campo], list):
            erro = [value[:] for value in erros[campo]][0]
        else:
            erro = erros[campo]

        lista.append(dict({"campo": campo, "erro": erro}))
        
    return lista

def dicionarioErrosValidacao(erros):
    dicionario = dict()
    for campo in erros:
        if campo=="status":
            continue

        erro = [value[:] for value in erros[campo]][0]
        dicionario[campo] = erro

    return dicionario


# Respostas Padrão do Django
def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, serializers.ValidationError):
           return RespostaErroDetalhado(response.status_code, listaErrosValidacao(exc.detail))

        response.data['status'] = response.status_code

        if "detail" in response.data:
            response.data['mensagem'] = response.data["detail"]
            del response.data["detail"]
        else:
            response.data['mensagem'] = "Eita! Algo está errado :("


    return response
