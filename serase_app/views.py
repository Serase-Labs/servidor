from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from django.db.models import F
from django.contrib.auth.models import User
from .models import PadraoMovimentacao
from .padroes_resposta import RespostaLista, RespostaStatus


class PadroesView(View):

    def get(self, request):
        ESCOLHAS_TIPO = ["R", "D"]

        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query = PadraoMovimentacao.objects.filter(cod_usuario=usuario)

        # Caso especificado o tipo de padrao
        if "tipo" in request.GET:
            tipo = request.GET["tipo"]

            if tipo not in ESCOLHAS_TIPO:
                return RespostaStatus(500, "Tipo inválido!")

            query = query.filter(receita_despesa=tipo)


        # Converte queryset em uma lista de dicionarios(objetos)
        lista = query.values("id", "descricao", "periodo", "dia_cobranca", "data_inicio", "data_fim", valor_padrao=F("valor"), categoria=F("cod_categoria__nome"), tipo=F("receita_despesa"))
        lista = list(lista)

        return RespostaLista(200, lista)