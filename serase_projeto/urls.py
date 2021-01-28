"""serase_projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from serase_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('padroes/', PadroesView.as_view(), name='padroes'),
    path('movimentacao/<int:id>/', InfoMovimentacao.as_view(), name='info_movimentacao'),
    path('movimentacoes/', MovimentacaoSimplesView.as_view(), name='movimentacoes'),
    path('status/', StatusServidorView.as_view(), name='status'),
    path('saldo/', SaldoView.as_view(), name='saldo'),
    url('inserirpadrao/$',InserirPadrao.as_view(),name='inserirpadrao'),
    path('usuario/', InformacoesUsuarioView.as_view(), name='usuario'),
    path('inserir_movimentacao',Insere_Mov.as_view(), name='insere_mov'),
    path('atualizar_movimentacao',AtualizacaoMovimentacao.as_view(), name='autaliza_mov'),
    path('relatorio/', include('serase_relatorio.urls')), # Inserir URLs antes dessa linha
]
