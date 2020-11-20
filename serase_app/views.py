from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from django.db.models import F
from django.contrib.auth.models import User
from .models import *
from .padroes_resposta import *
from .utils import *


class PadroesView(View):
    def get(self, request):
        VALORES_VALIDOS_TIPO = ["receita", "despesa"]

        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query = PadraoMovimentacao.objects.filter(cod_usuario=usuario)

        # Caso especificado o tipo de padrao
        if "tipo" in request.GET:
            tipo = request.GET["tipo"]

            if tipo not in VALORES_VALIDOS_TIPO:
                return RespostaStatus(500, "Tipo inválido!")

            query = query.filter(receita_despesa=tipo)


        # Converte queryset em uma lista de dicionarios(objetos)
        lista = query.values("id", "descricao", "periodo", "dia_cobranca", "data_inicio", "data_fim", valor_padrao=F("valor"), categoria=F("cod_categoria__nome"), tipo=F("receita_despesa"))
        lista = list(lista)

        return RespostaLista(200, lista)

class InfoMovimentacao(View):
    def get(self, request, id):
        #Juan é o usuario padrão no momento        
        usuario = User.objects.get(username="jv_eumsmo") 

        #Não tenho muita certeza do que eu estou fazendo
        info = Movimentacao.objects.filter(id=id)

        info_mov = info.values("cod_PadraoMovimentacao","valor_esperado","data_geracao","data_lancamento","valor_pago","descricao",categoria_nome=F("categoria__nome"))       
        info_mov = list(info_mov)

        return RespostaConteudo(200, info_mov)

        #Só tá funcionando pro usuário do momento, que é o Juan




class MovimentacaoSimplesView(View):
    def get(self, request):
        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query = Movimentacao.objects.filter(cod_usuario=usuario)

        # Filtragem para movimentação não pendentes
        query = query.filter(valor_pago__isnull=False)

        # Filtragem por tipo
        if "tipo" in request.GET:
            tipo = request.GET["tipo"]

            if tipo == "receita":
                query = query.filter(valor_pago__gte=0) # Valor positivo
            elif tipo == "despesa":
                query = query.filter(valor_pago__lt=0)  # Valor negativo
            else:
                return RespostaAtributoInvalido("tipo", tipo, ["receita", "despesa"])

        # Filtragem por categoria
        if "categoria" in request.GET:
            nome_categoria = request.GET["categoria"]
            query = query.filter(cod_categoria__nome=nome_categoria)

        # Filtragem por periodo
        if "data_inicial" in request.GET:
            try:
                data_inicial = converte_data_string(request.GET["data_inicial"])
            except:
                return RespostaFormatoDataInvalido()

            query = query.filter(data_lancamento__gte=data_inicial)

        if "data_final" in request.GET:
            try:
                data_final = converte_data_string(request.GET["data_final"])
            except:
                return RespostaFormatoDataInvalido()

            query = query.filter(data_lancamento__lte=data_final)

        # Gera lista de valores 
        lista = query.values("id", "descricao", "data_lancamento", "valor_pago")

        #paginacao(request, lista)


       # if is_paginacao:
        #    return RespostaPaginacao(200, list(lista), 5)
        #else:
        return RespostaLista(200, list(lista))