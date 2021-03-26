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
from serase_app.utils import *
from serase_app.serializers import *


# Movimentação

class MovimentacaoSimplesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user

        # Filtragem dos padrões do usuário atual
        query = Movimentacao.objects.filter(cod_usuario=usuario)
        # Filtragem para movimentação não pendentes
        query = query.filter(valor_pago__isnull=False)

        # Checa validade dos parametros
        validacao = FiltrarMovimentacaoSerializer(data=request.GET)
        validacao.is_valid(raise_exception=True)

        # Filtragem por tipo
        if "tipo" in request.GET:
            tipo = request.GET["tipo"]
            if tipo == "receita":
                query = query.filter(valor_pago__gte=0) # Valor positivo
            elif tipo == "despesa":
                query = query.filter(valor_pago__lt=0)# Valor negativo
    
        # Filtragem por categoria
        if "categoria" in validacao.validated_data:
            query = query.filter(cod_categoria=validacao.validated_data["categoria"])

        # Filtragem por periodo
        if "data_inicial" in validacao.validated_data:
            query = query.filter(data_lancamento__gte=validacao.validated_data["data_inicial"])

        if "data_final" in validacao.validated_data:
            query = query.filter(data_lancamento__lte=validacao.validated_data["data_final"])
        
        if "filtro" in request.GET:
            query = query.filter(descricao__contains=request.GET["filtro"]) 

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

        required_params(json_data, ["descricao", "valor_pago", "data_lancamento", "categoria"])
        validacao = ParametroMovimentacaoSerializer(data=json_data)
        validacao.is_valid(raise_exception=True)

        descricao = validacao.validated_data["descricao"]
        valor_pago = validacao.validated_data["valor_pago"]
        data_lancamento = validacao.validated_data["data_lancamento"]
        categoria = validacao.validated_data["categoria"]

        mov = Movimentacao(descricao=descricao, valor_pago=valor_pago, data_lancamento=data_lancamento, cod_usuario=usuario,cod_categoria=Categoria.objects.get(nome=categoria), cod_padrao=None)
        mov.save()
        return RespostaConteudo(200, model_to_dict(mov))
            

class MovimentacaoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        usuario = request.user

        #Filtrando movimentacao e usuario
        info = Movimentacao.objects.filter(cod_usuario=usuario,id=id)

        # Vendo se existe através do queryset
        if info.exists():
            # Converte queryset em uma lista que depois tá retornando só um objeto msm
            info_mov = info.values("cod_padrao","valor_esperado","valor_pago","data_geracao","data_lancamento","descricao",categoria=F("cod_categoria__nome"))
            info_mov = list(info_mov)
            return RespostaConteudo(200, info_mov[0])

        return RespostaStatus(400, "Movimentação inexistente!")

    def put(self,request,id):
        usuario = request.user
        info = Movimentacao.objects.filter(cod_usuario=usuario,id=id)

        if not info.exists():
            return RespostaStatus(400, "Movimentação inexistente!")

        json_data = json.loads(request.body)
        validacao = ParametroMovimentacaoSerializer(data=json_data)
        validacao.is_valid(raise_exception=True)

        movimentacao = info.first()

        if "descricao" in validacao.validated_data:
            movimentacao.descricao = validacao.validated_data["descricao"]
        if "valor_pago" in validacao.validated_data:
            movimentacao.valor_pago = validacao.validated_data["valor_pago"]
        if "data_lancamento" in validacao.validated_data:
            movimentacao.data_lancamento = validacao.validated_data["data_lancamento"]
        if "categoria" in validacao.validated_data:
            movimentacao.categoria = validacao.validated_data["categoria"]

        movimentacao.save()
            
        return RespostaConteudo(200,model_to_dict(movimentacao))

    def delete(self, request, id):
        usuario = request.user

        query = Movimentacao.objects.filter(cod_usuario=usuario,id=id)
        if query.exists():
            query.delete()
            return RespostaStatus(200,"Movimentação deletada.")             
        else:    
            return RespostaStatus(400,"Erro! Essa movimentação não existe.")         


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

