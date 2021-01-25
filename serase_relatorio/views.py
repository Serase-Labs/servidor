from django.shortcuts import render
from rest_framework.views import APIView

from serase_app.padroes_resposta import *
from .analise import analise_resumo

# Analises / Componentes

class ResumoAnaliseView(APIView):
    def get(self, request):
        periodo = request.GET["periodo"]
        return RespostaConteudo(200, analise_resumo(periodo))




# Relatórios

class RelatorioSemanalView(APIView):
    def get(self, request):
        periodo = "semana"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(periodo)
        })

class RelatorioMensalView(APIView):
    def get(self, request):
        periodo = "mes"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(periodo)
        })

class RelatorioAnualView(APIView):
    def get(self, request):
        periodo = "ano"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(periodo)
        })