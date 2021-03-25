# All Django Stuff
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

# All rest framework stuff
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# All python and dependences stuff
import json
from datetime import date
from decimal import Decimal

# All in this app stuff
from .utils import *

# All in other app stuff
from serase_app.models import *
from serase_app.padroes_resposta import *


# Movimentação

class MovimentacaoSimplesView(APIView):
    permission_classes = [IsAuthenticated]

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
                
                query = query.filter(valor_pago__lt=0)# Valor negativo
                
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
        
        if "filtro" in request.GET:
                    filtro = request.GET["filtro"]
                    query = query.filter(descricao__contains=filtro) 

        # Ordena query
        query = query.order_by("-data_lancamento")

        # Gera lista de valores
        lista = query.values("id", "descricao", "data_lancamento", "valor_pago")


        if "limite" in request.GET:
            return paginacao(request, lista)
        else:
            return RespostaLista(200, list(lista))

class InsereMovimentacaoView(APIView):
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get(self, request, id):

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
    permission_classes = [IsAuthenticated]

    def get(self, request, id):

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


# Saldo

class SaldoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        hoje = datetime.today()
        mes_ano = hoje
        
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



# Categoria

class CategoriaView(APIView):
   
    def get(self, request):
        query = Categoria.objects.all()
    
        lista = query.values_list("nome", flat=True)
        lista = list(lista)

        return RespostaLista(200, lista)



# Misc

class StatusServidorView(APIView):
    def get(self, request):
        return RespostaStatus(200, "Requisição feita com sucesso!")
    
    def post(self, request):

        if request.body:
            json_data = json.loads(request.body)
            for something in json_data:
                print(something, json_data[something])

        return RespostaStatus(200, "Requisição POST feita com sucesso!")
