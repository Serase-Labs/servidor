# All Django Stuff
from django.contrib.auth.models import User

# All rest framework stuff
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# All in this app stuff
from .analise import *
from .utils import validade_periodo, erro_periodo

# All in other app stuff
from serase_app.padroes_resposta import *



# Analises / Componentes

class ResumoAnaliseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, periodo):
        if not validade_periodo(periodo):
            return erro_periodo(periodo)

        usuario = request.user
        resposta = analise_resumo(usuario, periodo)

        return RespostaConteudo(200, resposta)

class CategoriaAnaliseView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, periodo):
        if not validade_periodo(periodo):
            return erro_periodo(periodo)

        usuario = request.user
        resposta = analise_categoria(usuario, periodo)

        return RespostaConteudo(200, resposta)

class GraficoSemanalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        resposta = grafico_semanal(usuario)

        return RespostaLista(200, resposta)

class GraficoCategoriaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, periodo):
        if not validade_periodo(periodo):
            return erro_periodo(periodo)

        usuario = request.user
        resposta = grafico_categoria(usuario, periodo)

        return RespostaLista(200, resposta)

class GraficoPadraoDespesaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, periodo):
        if not validade_periodo(periodo):
            return erro_periodo(periodo)

        usuario = request.user
        resposta = grafico_padrao_despesa(usuario, periodo)

        return RespostaLista(200, resposta)

class GraficoAnualDespesaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        resposta = grafico_anual_despesa(usuario)

        return RespostaConteudo(200, resposta)

class GraficoAnualSaldoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        usuario = request.user
        resposta = grafico_anual_saldo(usuario)

        return RespostaConteudo(200, resposta)

class GraficoMensalDespesaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        
        usuario = request.user
        resposta= grafico_mensal_despesa(usuario)

        return RespostaConteudo(200, resposta)
                        

# Relatórios

class RelatorioSemanalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        periodo = "semanal"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(usuario, periodo),
            "analises": analise_categoria(usuario, periodo),
            "grafico_semanal": grafico_semanal(usuario),
        })

class RelatorioMensalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        periodo = "mensal"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(usuario, periodo),
            "analises": analise_categoria(usuario, periodo),
        })

class RelatorioAnualView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        usuario = request.user
        periodo = "anual"

        return RespostaConteudo(200, {
            "resumo": analise_resumo(usuario, periodo),
            "analises": analise_categoria(usuario, periodo),
            "grafico_saldo": grafico_anual_saldo(usuario),
            "grafico_despesa_fixa": grafico_anual_despesa(usuario),
        })