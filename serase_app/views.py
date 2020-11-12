from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from django.db.models import F, Case, When, CharField, Value
from django.contrib.auth.models import User
from .models import PadraoMovimentacao
from .padroes_resposta import RespostaLista, RespostaStatus


class PadroesView(View):

    def get(self, request):
        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query = PadraoMovimentacao.objects.filter(usuario=usuario)

        # Caso especificado o tipo de padrao
        if "tipo" in request.GET:
            tipo = request.GET["tipo"]
            
            if tipo == "receita":
                receita_despesa = False
            elif tipo == "despesa":
                receita_despesa = True
            else:
                return RespostaStatus(500, "Tipo inválido!")

            query = query.filter(receita_despesa=receita_despesa)

        # Cria campo "tipo" que tem valor "despesa" quando receita_despesa for verdadeiro e "receita" quando for falso
        query = query.annotate(tipo=Case( 
            When(receita_despesa=True, then=Value("despesa")),
            When(receita_despesa=False, then=Value("receita")),
            output_field=CharField()
        ))

        # Converte queryset em uma lista de dicionarios(objetos)
        lista = query.values("id", "tipo", "descricao", "periodo", "dia_cobranca", "data_inicio", "data_fim", valor_padrao=F("valor"), categorias=F("categoria__nome") )
        lista = list(lista)

        return RespostaLista(200, lista)