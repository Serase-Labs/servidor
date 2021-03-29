from django.urls import path
from .views import *

urlpatterns = [
    path('movimentacao/<int:id>/', MovimentacaoView.as_view(), name='movimentacao'),
    path('movimentacoes/', MovimentacaoSimplesView.as_view(), name='movimentacoes'),
    path('movimentacao/',InsereMovimentacaoView.as_view(), name='insere_mov'),
    path('saldo/', SaldoView.as_view(), name='saldo'),
    path('categoria/', CategoriaView.as_view(), name='categoria'),
]