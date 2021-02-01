from django.shortcuts import render
from rest_framework.views import APIView

from serase_app.padroes_resposta import *
from .analise import *
from .utils import validade_periodo, erro_periodo

# Analises / Componentes



class ResumoAnaliseView(APIView):
    def get(self, request, periodo):
        if not validade_periodo(periodo):
            return erro_periodo(periodo)

        usuario = User.objects.get(username="jv_eumsmo")
        
        resposta = analise_resumo(usuario, periodo)

        return RespostaConteudo(200, resposta)

class CategoriaAnaliseView(APIView):
    def get(self, request, periodo):
        if not validade_periodo(periodo):
            return erro_periodo(periodo)

        usuario = User.objects.get(username="jv_eumsmo")
        
        resposta = analise_categoria(usuario, periodo)

        return RespostaConteudo(200, resposta)

class GraficoSemanalView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")

        resposta = grafico_semanal(usuario)

        return RespostaLista(200, resposta)

class GraficoCategoriaView(APIView):
    def get(self, request, periodo):
        if not validade_periodo(periodo):
            return erro_periodo(periodo)

        usuario = User.objects.get(username="jv_eumsmo")

        resposta = grafico_categoria(usuario, periodo)

        return RespostaLista(200, resposta)

class GraficoPadraoDespesaView(APIView):
    def get(self, request, periodo):
        if not validade_periodo(periodo):
            return erro_periodo(periodo)

        usuario = User.objects.get(username="jv_eumsmo")

        resposta = grafico_padrao_despesa(usuario, periodo)

        return RespostaLista(200, resposta)

class GraficoAnualDespesaView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")

        resposta = grafico_anual_despesa(usuario)

        return RespostaConteudo(200, resposta)

# Relatórios

class RelatorioSemanalView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")
        periodo = "semanal"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(usuario, periodo),
            "analises": analise_categoria(usuario, periodo),
            "grafico_semanal": grafico_semanal(usuario),
        })

class RelatorioMensalView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")
        periodo = "mensal"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(usuario, periodo),
            "analises": analise_categoria(usuario, periodo),
        })

class RelatorioAnualView(APIView):
    def get(self, request):
        usuario = User.objects.get(username="jv_eumsmo")
        periodo = "anual"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(usuario, periodo),
            "analises": analise_categoria(usuario, periodo),
            "grafico_despesa_fixa": grafico_anual_despesa(usuario),
        })