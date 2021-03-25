from django.urls import path
from .views import *

urlpatterns = [
    path('usuario/logado/',UsuarioLogadoView.as_view(),name='UserLogado'),
    path('usuario/', InformacoesUsuarioView.as_view(), name='usuario'),
    path('cadastro/',CadastrarUsuarioView.as_view(),name='CadastrarUsuario'), 
    path('login/', LoginView.as_view(),name='Login'),
    path('logout/',LogoutView.as_view(),name='Logout'),
]