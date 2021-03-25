from django.urls import path
from .views import *

urlpatterns = [
    path('padrao/', InserirPadraoView.as_view(), name='insere_padrao'),
    path('padrao/<int:id>/',  PadraoView.as_view(), name='padrao'),
    path('padroes/',PadroesView.as_view(),name="padroes"),
    path('divida/',InserirDividaView.as_view(),name="insere_divida"),
    path('dividas/',FiltrarDividasView.as_view(), name='filtra_divida'),
    path('divida/<int:id>/',DividaView.as_view(),name="divida"),
    path('cobrancas/', CobrancaView.as_view(), name='cobranca'),
    path('pagamento/<int:id>/',PagarPadraoView.as_view(),name='pagarpadrao'),
]