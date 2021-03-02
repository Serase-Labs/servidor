from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from django.db.models import F, Sum
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from django.contrib.auth import login,logout, authenticate

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from decimal import Decimal
from rest_framework.views import APIView
import json
from .models import *
from .padroes_resposta import *
from .utils import *
import json
from .serializers import *


# Views sobre Padrão

class InserirPadraoView(APIView):
    def post(self, request):
        usuario = request.user
        json_data = json.loads(request.body)

        tipo= json_data["tipo"]
        descricao = json_data["descricao"]
        periodo = json_data["periodo"]
        valor =json_data["valor"]
        dia_cobranca = json_data["dia_cobranca"]
        data_inicio  = json_data["data_inicio"]
        data_fim= json_data["data_fim"]
        categoria= json_data["categoria"]

        if Categoria.objects.filter(nome=categoria).exists():
            label = PadraoMovimentacao.objects.create(receita_despesa=tipo,descricao=descricao,periodo=periodo, valor=valor, dia_cobranca=dia_cobranca,data_inicio=data_inicio,data_fim=data_fim, cod_usuario=usuario,cod_categoria=Categoria.objects.get(nome=categoria))
            return RespostaConteudo(200, model_to_dict(label))
        else:
            return RespostaStatus(400, "Categoria Inexistente!")

class PadraoView(APIView):
    def get(self, request, id):

        #Pegando o nome do usuário 
        usuario = request.user
        #Filtrando movimentacao e usuario 
        query = PadraoMovimentacao.objects.filter(cod_usuario=usuario,id=id)
        if query:
            lista = query.values("id", "descricao", "periodo", "dia_cobranca", "data_inicio", "data_fim", valor_padrao=F("valor"), categoria=F("cod_categoria__nome"), tipo=F("receita_despesa"))
            lista = list(lista)
            return RespostaConteudo(200,lista)             
        else:    
            return RespostaStatus(400,"Erro! esse id não está cadastrado")
    #def put(self,request,id):

        

    def delete(self, request, id):
        usuario = request.user
        id_padrao = id

        query = PadraoMovimentacao.objects.filter(cod_usuario=usuario,id=id_padrao)
        if query:
            query.delete()
            return RespostaStatus(200,"Padrao Deletado")             
        else:    
            return RespostaStatus(400,"Erro! Esse id não existe")        

        
class PadroesView(APIView):
    def get(self, request):
        VALORES_VALIDOS_TIPO = ["receita", "despesa"]
        usuario = request.user

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

class MovimentacaoSimplesView(APIView):
    def get(self, request):
        # Usuario padrão temporário (até implementado o login)
        usuario = request.user
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
    def post(self, request):
        usuario = request.user
        json_data = json.loads(request.body)

        descricao = json_data["descricao"]
        valor_pago = json_data["valor_pago"]
        data_lancamento  = json_data["data_lancamento"]
        categoria = json_data["categoria"]

        if Categoria.objects.filter(nome=categoria).exists():
            label = Movimentacao.objects.create(descricao=descricao, valor_pago=valor_pago, data_lancamento=data_lancamento, cod_usuario=usuario,cod_categoria=Categoria.objects.get(nome=categoria), cod_padrao=None)
            return RespostaConteudo(200, model_to_dict(label))
        else:
            return RespostaStatus(400, "Categoria Inexistente!")

class MovimentacaoView(APIView):
    def get(self, request, id):

        #Pegando o nome do usuário que nesse caso é o Juan (usuario padrão no momento)
        usuario = request.user
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
    
    def put(self,request,id):

        usuario = request.user
        info = Movimentacao.objects.filter(cod_usuario=usuario,id=id)

        json_data = json.loads(request.body)

        descricao = json_data["descricao"]
        valor_pago = json_data["valor_pago"]
        data_lancamento  = json_data["data_lancamento"]
        categoria = json_data["categoria"]

        data_lancamento = datetime.strptime(data_lancamento, '%Y-%m-%d')
        valor_pago = Decimal(valor_pago)

        if Categoria.objects.filter(nome=categoria).exists():
         
            mov_att = Movimentacao(id=id, descricao=descricao, valor_pago=valor_pago, data_lancamento=data_lancamento, cod_usuario=usuario,cod_categoria=Categoria.objects.get(nome=categoria), cod_padrao=None)
            mov_att.save()
            
            return RespostaConteudo(200,model_to_dict(mov_att))

        else:
            return RespostaStatus(404, "Categoria Inexistente!")

    def delete(self, request, id):
        usuario = request.user
        id_movimentacao = id

        query = Movimentacao.objects.filter(cod_usuario=usuario,id=id_movimentacao)
        if query:
            query.delete()
            return RespostaStatus(200,"Movimentacao Deletada")             
        else:    
            return RespostaStatus(400,"Erro! Esse id não existe")         


# Views sobre Saldo

class SaldoView(APIView):
    def get(self, request):
        hoje = mes_ano_atual()
        mes_ano = hoje
        
        # Usuario padrão temporário (até implementado o login)
        usuario = request.user

        # Filtragem por mes_ano
        if "mes_ano" in request.GET:
            try:
                mes_ano = converte_mes_ano_string(request.GET["mes_ano"])
            except:
                return RespostaFormatoDataInvalido()

            if mes_ano > hoje:
                return RespostaStatus(500, "Mês/ano deve ser menor ou igual ao da data atual!")



        saldo_mes, saldo_total = calcular_saldo(usuario, mes_ano, hoje)

        return RespostaConteudo(200, {
            "mes_ano": mes_ano.strftime("%Y-%m"),
            "mes": round(saldo_mes, 2),
            "total": round(saldo_total, 2),
        })


# Views sobre Categoria

class CategoriaView(APIView):
   
    def get(self, request):
        query = Categoria.objects.all()
    
        lista = query.values_list("nome", flat=True)
        lista = list(lista)

        return RespostaLista(200, lista)


# Views relacionadas ao Login

class CadastrarUsuarioView(APIView):
    def post (self,request): 
        json_data = json.loads(request.body)
        nome = json_data['nome']
        email=json_data['email']
        senha = json_data['senha'] 
        aux_usuario=User.objects.filter(email=email)
        if aux_usuario:
            return RespostaStatus(400,"Erro! Usario já cadastrado")
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
            return RespostaStatus(400, "Senha ou usuario invalidos ")

class InformacoesUsuarioView(APIView):
    def get(self, request):
        # Usuario padrão temporário (até implementado o login)
        usuario = request.user
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
        usuario= User.objects.get(email=email)
        nome = usuario.get_username()
        user = authenticate(request, username=nome, password=senha)
        
        
       # nomeUsuario= User.objects.get_username()
        if user is not None:
            login(request, user)
            token = Token.objects.get(user=usuario)

            return RespostaConteudo(200, {
                "nome": usuario.get_full_name(),
                "email": usuario.email,
                "token": "Token "+str(token),
            })
        else:
            return RespostaStatus(400, "Senha ou usuario invalidos!")    

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
