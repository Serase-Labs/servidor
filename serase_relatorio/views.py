from django.shortcuts import render
from rest_framework.views import APIView

from serase_app.padroes_resposta import *
from .analise import *

# Analises / Componentes

class ResumoAnaliseView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")
        periodo = request.GET["periodo"]
        
        resposta = analise_resumo(usuario, periodo)

        return RespostaConteudo(200, resposta)

class CategoriaAnaliseView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")
        periodo = request.GET["periodo"]
        
        resposta = analise_categoria(usuario, periodo)

        return RespostaConteudo(200, resposta)


# Relatórios

class RelatorioSemanalView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")
        periodo = "semana"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(usuario, periodo),
            "analises": analise_categoria(usuario, periodo),
        })

class RelatorioMensalView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")
        periodo = "mes"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(usuario, periodo),
            "analises": analise_categoria(usuario, periodo),
        })

class RelatorioAnualView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")
        periodo = "ano"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(usuario, periodo),
            "analises": analise_categoria(usuario, periodo),
        })