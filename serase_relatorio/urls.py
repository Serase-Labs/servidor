from django.urls import path, include
from .views import *
from serase_app.views import StatusServidorView

# Para acessar as urls deste arquivo, adicione na frente "relatorio/", por exemplo conseguimos acessar a url "categoria" através de "relatorio/categoria"
urlpatterns = [
    path('analise/', include([
        path('resumo/<str:periodo>/', ResumoAnaliseView.as_view(), name='analise_resumo'),
        path('categoria/<str:periodo>/', CategoriaAnaliseView.as_view(), name='analise_categoria'),
    ])),
    path('grafico/', include([
        path('categoria/<str:periodo>/', GraficoCategoriaView.as_view(), name='grafico_categoria'),
        path('padrao/<str:periodo>/', GraficoPadraoDespesaView.as_view(), name='grafico_padrao'),
        path('semanal/', GraficoSemanalView.as_view(), name='grafico_semanal'),
        path('despesa/anual/', GraficoAnualDespesaView.as_view(), name='grafico_despesa_anual'),
        path('saldo/anual/', GraficoAnualSaldoView.as_view(), name='grafico_saldo_anual'),
    ])),
    path('relatorio/', include([
        path('semanal/', RelatorioSemanalView.as_view(), name='relatorio_semanal'),
        path('mensal/', RelatorioMensalView.as_view(), name='relatorio_mensal'),
        path('anual/', RelatorioAnualView.as_view(), name='relatorio_anual'),
    ])),
]
