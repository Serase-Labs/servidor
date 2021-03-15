from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from django.db.models import F, Sum, Case, When, CharField, Value
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
from decimal import Decimal


# Views sobre cobranças (mudar para outro app futuramente)

def create_cobranca(padrao, data):
    # se padrão mensal
    data_geracao = business_days_in_month(data, padrao.dia_cobranca)
    
    cobranca = Movimentacao(descricao=padrao.descricao, valor_esperado=padrao.valor, data_geracao=data_geracao, cod_usuario=padrao.cod_usuario, cod_categoria=padrao.cod_categoria, cod_padrao=padrao)
    return cobranca


def gerar_cobranca(padrao):
    data_ultima_cobranca = padrao.ultima_cobranca.data_geracao
    hoje = date.today()

    # Vetor que armazenará novas cobranças caso sejam feitas
    cobrancas_criadas = []

    # Checa periodo do padrão e se há novas cobranças a serem feitas

    if padrao.periodo == "anual" and data_ultima_cobranca.year < hoje.year:
        print("Cobrança gerada por padrão anual não esta disponivel no atual momento!")
    elif padrao.periodo == "mensal" and data_ultima_cobranca < hoje: # Cobrança mensal e ultima cobrança não foi nesse mes
        # Código ainda só considera cobranças de padrão normal, ignorando as de divida.
        while data_ultima_cobranca < hoje.replace(day=1):
            data_ultima_cobranca = data_ultima_cobranca + relativedelta(months=1)
            data_ultima_cobranca = data_ultima_cobranca.replace(day=1)
            aux = create_cobranca(padrao, data_ultima_cobranca)
            data_ultima_cobranca = aux.data_geracao
            
            if data_ultima_cobranca <= hoje:
                cobrancas_criadas.append(aux)
    elif padrao.periodo == "semanal" and data_ultima_cobranca.year <= hoje.year and week_num(data_ultima_cobranca) < week_num(hoje):
        print("Cobrança gerada por padrão semanal não esta disponivel no atual momento!")


    Movimentacao.objects.bulk_create(cobrancas_criadas)
    return cobrancas_criadas


class CobrancaView(APIView):
    def get(self, request):
        VALORES_VALIDOS_TIPO = ["receita", "despesa"]
        VALORES_VALIDOS_SITUACAO = ["pendente", "paga"]
        usuario = request.user

        # Cobranças são movimentações geradas por padrões
        query = Movimentacao.objects.filter(cod_usuario=usuario, cod_padrao__isnull=False)

        if "situacao" in request.GET:
            situacao = request.GET["situacao"]

            if tipo not in VALORES_VALIDOS_SITUACAO:
                return RespostaAtributoInvalido("situacao", tipo, VALORES_VALIDOS_TIPO)

            if situacao == "paga":
                query = query.filter(data_lancamento__isnull=False)
            elif situacao == "pendente":
                query = query.filter(data_lancamento__isnull=True)
            # elif situacao == "...":
        
        if "tipo" in request.GET:
            tipo = request.GET["tipo"]

            if tipo not in VALORES_VALIDOS_TIPO:
                return RespostaAtributoInvalido("tipo", tipo, VALORES_VALIDOS_TIPO)

            query = query.filter(cod_padrao__receita_despesa=tipo)

        if "cod_padrao" in request.GET:
            tipo = request.GET["cod_padrao"]
            #TO-DO: adicionar if pra checar se padrao existe
            query = query.filter(cod_padrao=cod_padrao)

        # Converte queryset em uma lista de dicionarios(objetos)
        query = query.annotate(situacao=Case(
            When(data_lancamento__isnull=False, then=Value("paga")),
            When(data_lancamento__isnull=True, then=Value("pendente")),
            output_field=CharField()
        ))
        lista = query.values("id", "descricao", "valor_esperado", "data_geracao", "situacao", "cod_padrao", categoria=F("cod_categoria__nome"))
        lista = list(lista)

        return RespostaLista(200, lista)


# Views sobre Padrão

class InserirPadrao(generics.ListCreateAPIView):
   queryset = PadraoMovimentacao.objects.all()
   serializer_class = PadraoMovimentacaoSerializer

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
    def post(self, request):
        usuario = User.objects.get(username="jv_eumsmo")
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


class MovimentacaoView(APIView):
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

    def put(self,request,id):

        usuario = User.objects.get(username="jv_eumsmo")
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
        usuario = User.objects.get(username="jv_eumsmo")
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
        usuario = User.objects.get(username="jv_eumsmo")

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
        if User.objects.get(username="jv_eumsmo").is_authenticated:
            username = User.objects.get(username="jv_eumsmo").get_username()
            return RespostaStatus(200, username)  
        else:
            return RespostaStatus(400, "Senha ou usuario invalidos ")

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

