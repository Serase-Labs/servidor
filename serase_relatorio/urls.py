from django.urls import path, include
from .views import *
from serase_app.views import StatusServidorView

# Para acessar as urls deste arquivo, adicione na frente "relatorio/", por exemplo conseguimos acessar a url "categoria" através de "relatorio/categoria"
urlpatterns = [
    path('analise/resumo/', ResumoAnaliseView.as_view(), name='analise_resumo'),
    path('semanal', RelatorioSemanalView.as_view(), name='relatorio_semanal'),
    path('mensal', RelatorioMensalView.as_view(), name='relatorio_mensal'),
    path('anual', RelatorioAnualView.as_view(), name='relatorio_anual'),
]
