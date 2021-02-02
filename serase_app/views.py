from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from django.db.models import F, Sum
from django.contrib.auth.models import User

from django.contrib.auth import login,logout, authenticate

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework.views import APIView
import json
from .models import *
from .padroes_resposta import *
from .utils import *
import json
from .serializers import *


# Views sobre Padrão

class PadraoView(APIView):
    def post(self,request):
      serializer= PadraoMovimentacaoSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ###Pegar o codigo do usuario que esta logado
    def delete(self,request):  
        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query = Movimentacao.objects.filter(cod_usuario=usuario)

        count = PadraoMovimentacao.objects.filter(cod_usuario=usuario).delete()
        return Response(status= HTTP_200_OK)
        
class PadroesView(APIView):
    def get(self, request):
        VALORES_VALIDOS_TIPO = ["receita", "despesa"]

        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query = PadraoMovimentacao.objects.filter(cod_usuario=usuario)

        # Caso especificado o tipo de padrao
        if "tipo" in request.GET:
            tipo = request.GET["tipo"]

            if tipo not in VALORES_VALIDOS_TIPO:
                return RespostaAtributoInvalido("tipo", tipo, VALORES_VALIDOS_TIPO)

            query = query.filter(receita_despesa=tipo)


        # Converte queryset em uma lista de dicionarios(objetos)
        lista = query.values("id", "descricao", "periodo", "dia_cobranca", "data_inicio", "data_fim", valor_padrao=F("valor"), categoria=F("cod_categoria__nome"), tipo=F("receita_despesa"))
        lista = list(lista)

        return RespostaLista(200, lista)
    

# Views sobre Movimentação

class InfoMovimentacaoView(APIView):
    def get(self, request, id):

        #Pegando o nome do usuário que nesse caso é o Juan (usuario padrão no momento)
        usuario = User.objects.get(username="jv_eumsmo")

        #Filtrando movimentacao e usuario = pegando a movimentacao do usuario que ele estiver logado
        info = Movimentacao.objects.filter(cod_usuario=usuario,id=id)

        #vendo se retorna alguma coisa através do queryset
        if len(info) > 0 :

            # Converte queryset em uma lista que depois tá retornando só um objeto msm
            info_mov = info.values("cod_padrao","valor_esperado","valor_pago","data_geracao","data_lancamento","descricao",categoria=F("cod_categoria__nome"))
            info_mov = list(info_mov)

        #vendo se não retorna nada
        if len(info) == 0:

            return RespostaStatus(404, "Movimentação Inexistente!")

        return RespostaConteudo(200, info_mov[0])

class MovimentacaoSimplesView(APIView):
    def get(self, request):
        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query = Movimentacao.objects.filter(cod_usuario=usuario)

        # Filtragem para movimentação não pendentes
        query = query.filter(valor_pago__isnull=False)

        # Filtragem por tipo
        if "tipo" in request.GET:
            tipo = request.GET["tipo"]

            if tipo == "receita":
                query = query.filter(valor_pago__gte=0) # Valor positivo
            elif tipo == "despesa":
                query = query.filter(valor_pago__lt=0)  # Valor negativo
            else:
                return RespostaAtributoInvalido("tipo", tipo, ["receita", "despesa"])

        # Filtragem por categoria
        if "categoria" in request.GET:
            nome_categoria = request.GET["categoria"]
            query = query.filter(cod_categoria__nome=nome_categoria)

        # Filtragem por periodo
        if "data_inicial" in request.GET:
            try:
                data_inicial = converte_data_string(request.GET["data_inicial"])
            except:
                return RespostaFormatoDataInvalido()

            query = query.filter(data_lancamento__gte=data_inicial)

        if "data_final" in request.GET:
            try:
                data_final = converte_data_string(request.GET["data_final"])
            except:
                return RespostaFormatoDataInvalido()

            query = query.filter(data_lancamento__lte=data_final)

        # Ordena query
        query = query.order_by("-data_lancamento")

        # Gera lista de valores
        lista = query.values("id", "descricao", "data_lancamento", "valor_pago")


        if "limite" in request.GET:
            return paginacao(request, lista)
        else:
            return RespostaLista(200, list(lista))

class InsereMovimentacaoView(APIView):

    def post(self,request):
    
        usuario = User.objects.get(username="jv_eumsmo") 

        json_data = json.loads(request.body)

        descricao = json_data["descricao"]
        valor_esperado = json_data["valor_esperado"]
        valor_pago = json_data["valor_pago"]
        data_geracao = json_data["data_geracao"]
        data_lancamento  = json_data["data_lancamento"]

        label = Movimentacao.objects.create(description=descricao, valor_esperado=valor_esperado,valor_pago=valor_pago,
        data_geracao=data_geracao,data_lancamento=data_lancamento, cod_usuario=usuario, categoria=F("cod_categoria__nome"), cod_padrao=0)

        return RespostaConteudo(200, label)


# Views sobre Saldo

class SaldoView(APIView):
    def get(self, request):
        hoje = mes_ano_atual()

        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query_saldo = Saldo.objects.filter(cod_usuario=usuario)


        saldo_mes = None
        saldo_total = None
        mes_ano = None

        # Filtragem por mes_ano
        if "mes_ano" in request.GET:
            try:
                mes_ano = converte_mes_ano_string(request.GET["mes_ano"])
            except:
                return RespostaFormatoDataInvalido()

            if mes_ano > hoje:
                return RespostaStatus(500, "Mês/ano deve ser menor ou igual ao da data atual!")


        if mes_ano==None:
            mes_ano = hoje
        
        saldo_mes, saldo_total = calcular_saldo(usuario, mes_ano, hoje)
        
        # Filtra por saldos anteriores ao mes_ano
        query_saldo = query_saldo.filter(mes_ano__lt=mes_ano.replace(day=1))
        saldo_total = query_saldo.aggregate(Sum("saldo"))["saldo__sum"] or 0

        saldo_total+=saldo_mes


        return RespostaConteudo(200, {
            "mes_ano": mes_ano.strftime("%Y-%m"),
            "mes": round(saldo_mes, 2),
            "total": round(saldo_total, 2),
        })


# Views sobre Categoria

class CategoriaView(APIView):
    """docstring for CategoriaView"""
    def get(self, request):
        query = Categoria.objects.all()
        '''if "categoria" in request.GET:
            nome_categoria = request.GET["categoria"]
            query = query.filter(cod_categoria__nome=nome_categoria)
        '''
        lista = query.values_list("nome", flat=True)
        lista = list(lista)

        return RespostaLista(200, lista)


# Views relacionadas ao Login

class CadastrarUsuarioView(APIView):
    def post (self,request):
        '''try:   
            json_data = json.loads(request.body)
            email=json_data['email']
            aux_usuario=User.objects.get(email)
            if aux_usuario:
                return render(request,"Erro! Usario já cadastrado")
        except User.DoesNotExist:'''
        json_data = json.loads(request.body)
        
        nome = json_data['nome']
        email=json_data['email']
        senha = json_data['senha']
        novo_usuario = User.objects.create_user(username=nome,email=email,password=senha)
        novo_usuario.save()
        return RespostaStatus(200, "Requisição feita com sucesso!")     

class UsuarioLogadoView(APIView):
    def get(self,request):
        username = None
        if request.user.is_authenticated:
            username = request.user.get_username()
            return RespostaStatus(200, username)  
        else:
            return RespostaStatus(200, "Senha ou usuario invalidos ")

class InformacoesUsuarioView(APIView):
    def get(self, request):
        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        s, saldo_total = calcular_saldo(usuario)

        return RespostaConteudo(200, {
            "nome": usuario.get_full_name(),
            "email": usuario.email,
            "saldo": round(saldo_total, 2),
        })

class LoginView(APIView):#Por enquanto somente o do juan 
    def post(self,request):
        json_data = json.loads(request.body)
        email=json_data['email']
        senha = json_data['senha']
        Usuario= User.objects.get(email=email)
        nome =Usuario.get_username()
        user = authenticate(request, username=nome, password=senha)
        
        
       # nomeUsuario= User.objects.get_username()
        if user is not None:
            login(request, user)
            return RespostaStatus(200, "Requisição feita com sucesso!")
        else:
            return RespostaStatus(200, "Senha ou usuario invalidos ")    

class LogoutView(APIView):         
    def get(self,request):
        logout(request)
        return RespostaStatus(200, "Requisição feita com sucesso!")


# Misc Views

class StatusServidorView(APIView):
    def get(self, request):
        return RespostaStatus(200, "Requisição feita com sucesso!")
    
    def post(self, request):

        if request.body:
            json_data = json.loads(request.body)
            for something in json_data:
                print(something, json_data[something])

        return RespostaStatus(200, "Requisição POST feita com sucesso!")
