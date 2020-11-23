from django.http import JsonResponse

# Padrões de Respostas

def Resposta(status, conteudo):
    return JsonResponse(conteudo, status=status, json_dumps_params={'indent': 2, 'ensure_ascii':False})

def RespostaStatus(status,mensagem:str):
    return Resposta(status, {"status": status, "mensagem": mensagem})

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

    
    return RespostaStatus(500, mensagem)
    
def RespostaFormatoDataInvalido():
    return RespostaStatus(500, "Formato incorreto para data, o formato esperado é YYYY-MM-DD")