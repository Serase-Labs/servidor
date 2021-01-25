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

from rest_framework.views import APIView

from .models import *
from .padroes_resposta import *
from .utils import *
from .serializers import *



class PadroesView(View):
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


class InfoMovimentacao(View):
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

            return RespostaStatus(404, "Movimentação Inexiste!")

        return RespostaConteudo(200, info_mov[0])


class MovimentacaoSimplesView(View):
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


class StatusServidorView(View):
    def get(self, request):
        return RespostaStatus(200, "Requisição feita com sucesso!")


class SaldoView(View):
    def get(self, request):
        hoje = mes_ano_atual()

        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query_saldo = Saldo.objects.filter(cod_usuario=usuario)


        saldo_mes = None
        saldo_total = None

        # Filtragem por mes_ano
        if "mes_ano" in request.GET:
            try:
                mes_ano = converte_mes_ano_string(request.GET["mes_ano"])
            except:
                return RespostaFormatoDataInvalido()

            if mes_ano > hoje:
                return RespostaStatus(500, "Mês/ano deve ser menor ou igual ao da data atual!")

            # Caso o mês/ano não seja o atual
            if not is_mes_ano_igual(mes_ano, hoje):
                saldo = query_saldo.get(mes_ano__month=mes_ano.month, mes_ano__year=mes_ano.year)
                saldo_mes = saldo.saldo

        # Calcula saldo caso mês seja o mês atual, uma vez que não existe um objeto Saldo
        if saldo_mes==None:
            mes_ano = hoje
            query_movimentacao = Movimentacao.objects.filter(cod_usuario=usuario, valor_pago__isnull=False)
            query_movimentacao = query_movimentacao.filter(data_lancamento__year=mes_ano.year, data_lancamento__month=mes_ano.month)
            saldo_mes = query_movimentacao.aggregate(Sum("valor_pago"))["valor_pago__sum"] or 0

        # Filtra por saldos anteriores ao mes_ano
        query_saldo = query_saldo.filter(mes_ano__lt=mes_ano.replace(day=1))
        saldo_total = query_saldo.aggregate(Sum("saldo"))["saldo__sum"] or 0

        saldo_total+=saldo_mes


        return RespostaConteudo(200, {
            "mes_ano": mes_ano.strftime("%Y-%m"),
            "mes": round(saldo_mes, 2),
            "total": round(saldo_total, 2),
        })

        return RespostaLista(200, lista)

class CategoriaView(View):
    """docstring for CategoriaView"""
    def get(self, request):
        query = Categoria.objects.all()
        '''if "categoria" in request.GET:
            nome_categoria = request.GET["categoria"]
            query = query.filter(cod_categoria__nome=nome_categoria)
        '''
        lista = query.values("nome")
        lista = list(lista)

        return RespostaLista(200, lista)

class PostPadrao(APIView):
    def post(self,request):
      serializer= PadraoMovimentacaoSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeletePadrao(APIView):
    ###Pegar o codigo do usuario que esta logado

        
                
    def delete(self,request):  
        # Usuario padrão temporário (até implementado o login)
        usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query = Movimentacao.objects.filter(cod_usuario=usuario)

        count = PadraoMovimentacao.objects.filter(cod_usuario=usuario).delete()
        return Response(status= HTTP_200_OK)


#Classe de criação de usuario provisoria;Terminar quando definir commo a autenticação ira funcionar.

class CadastrarUsuario(APIView):
    def post(self,request):
        try:   

            json_data = json.loads(request.body)
            email=json_data['email']
            aux_usuario=User.objects.get(email)
            if aux_usuario:
                return render(request,"Erro! Usario já cadastrado")
        except User.DoesNotExist:
            nome = json_data['nome']
            email=json_data['email']
            senha = json_data['senha']
            novo_usuario = User.objects.create_user(nome,email,senha)
            novo_usuario.save()
            return RespostaStatus(200, "Requisição feita com sucesso!")

'''class EstaLogado (APIView):#por enquanto ONLY juan
    def get(self,request):
        if request.user.is_authenticated:
            return  User.objects.filter(username="jv_eumsmo").values()
        else:
            return RespostaStatus(200, "Senha ou usuario invalidos ")    
      
class UserLogado(APIView):
    def get(self,request):
         usuario = User.objects.get(username="jv_eumsmo")

        # Filtragem dos padrões do usuário atual
        query = Movimentacao.objects.filter(cod_usuario=usuario)

        return  RespostaStatus(200,User.objects.filter(username="jv_eumsmo").values())
  '''

class Logout(APIView)         
    def deslogar(request):
        logout(request)
        return RespostaStatus(200, "Requisição feita com sucesso!")      
class Login(APIView):#Por enquanto somente o do juan 
    def my_view(request):
        json_data = json.loads(request.body)
        email=json_data['email']
        senha = json_data['senha']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return RespostaStatus(200, "Requisição feita com sucesso!")
        else:
            return RespostaStatus(200, "Senha ou usuario invalidos ")    





