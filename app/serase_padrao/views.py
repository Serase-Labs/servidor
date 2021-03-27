# All Django Stuff
from django.db.models import F, Case, When, CharField, Value
from django.forms.models import model_to_dict

# All rest framework stuff
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# All python and dependences stuff
from dateutil.rrule import *
from datetime import date, timedelta
import json

# All in other app stuff
from serase_app.models import *
from serase_app.padroes_resposta import *
from serase_app.utils import *
from serase_app.serializers import *


# Padrão

class InserirPadraoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = request.user
        json_data = json.loads(request.body)

        required_params(json_data, ["tipo", "descricao", "periodo", "dia_cobranca", "categoria"])
        validacao = ParametroPadraoMovimentacaoSerializer(data=json_data)
        validacao.is_valid(raise_exception=True)


        tipo = validacao.validated_data["tipo"]
        descricao = validacao.validated_data["descricao"]
        periodo = validacao.validated_data["periodo"]
        dia_cobranca = validacao.validated_data["dia_cobranca"]
        categoria = validacao.validated_data["categoria"]

        padrao = PadraoMovimentacao(receita_despesa=tipo,descricao=descricao,periodo=periodo, dia_cobranca=dia_cobranca, cod_usuario=usuario,cod_categoria=categoria)

        if "valor" in validacao.validated_data:
            padrao.valor = validacao.validated_data["valor"]

        if "data_fim" in validacao.validated_data:
            padrao.data_fim = validacao.validated_data["data_fim"]

        padrao.save()

        dic = model_to_dict(padrao, fields=["id", "descricao", "periodo", "dia_cobranca", "data_geracao", "data_fim", "valor"])
        dic["categoria"] = categoria.nome
        dic["tipo"] = tipo

        return RespostaConteudo(200, dic)

class PadraoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        usuario = request.user
        query = PadraoMovimentacao.objects.filter(cod_usuario=usuario,id=id)

        if query.exists():
            lista = query.values("id", "descricao", "periodo", "dia_cobranca", "data_geracao", "data_fim", "valor", categoria=F("cod_categoria__nome"), tipo=F("receita_despesa"))
            lista = list(lista)
            return RespostaConteudo(200, lista[0])        
        else:    
            return RespostaStatus(400,"Padrão inexistente!")
     
    def put(self,request,id):
        usuario = request.user
        json_data = json.loads(request.body)

        query = PadraoMovimentacao.objects.filter(id=id,cod_usuario=usuario)

        if not query.exists():
            return RespostaStatus(400, "Padrão inexistente!")

        validacao = ParametroPadraoMovimentacaoSerializer(data=json_data)
        validacao.is_valid(raise_exception=True)
        data = validacao.validated_data

        padrao = query.first()
        
        if "tipo" in data:
            padrao.receita_despesa = data["tipo"]
        if "periodo" in data:
            padrao.periodo = data["periodo"]
        if "descricao" in data:
            padrao.descricao = data["descricao"]
        if "valor" in data:
            padrao.valor = data["valor"]   
        if "dia_cobranca" in data:
            padrao.dia_cobranca = jdata["dia_cobranca"]
        if "data_fim" in data:
            padrao.data_fim = data["data_fim"]            
        if "categoria" in data:
            padrao.categoria = data["categoria"]

        padrao.save()

        dic = model_to_dict(padrao, fields=["id", "descricao", "periodo", "dia_cobranca", "data_geracao", "data_fim", "valor"])
        dic["categoria"] = padrao.cod_categoria.nome
        dic["tipo"] = padrao.receita_despesa
        
        return RespostaConteudo(200,dic)  
    
    def delete(self, request, id):
        usuario = request.user

        query = PadraoMovimentacao.objects.filter(cod_usuario=usuario,id=id)

        if query.exists():
            query.delete()
            return RespostaStatus(200,"Padrao deletado.")             
        else:    
            return RespostaStatus(400,"Padrão inexistente!")        
    
class PadroesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user

        # Filtragem dos padrões do usuário atual
        query = PadraoMovimentacao.objects.filter(cod_usuario=usuario)

        query = query.exclude(receita_despesa="divida")

        validacao = FiltrarPadraoMovimentacaoSerializer(data=request.GET)
        validacao.is_valid(raise_exception=True)
        data = validacao.validated_data


        if "tipo" in data:
            query = query.filter(receita_despesa=data["tipo"])
        if "categoria" in data:
            query = query.filter(cod_categoria=data["categoria"])


        # Converte queryset em uma lista de dicionarios(objetos)
        lista = query.values("id", "descricao", "periodo", "dia_cobranca", "data_geracao", "data_fim", "valor", categoria=F("cod_categoria__nome"), tipo=F("receita_despesa"))
        lista = list(lista)

        return RespostaLista(200, lista)



# Cobrança

def calc_weekday(day):
    return (day+5)%7

def gerar_cobranca(padrao, create=False):
    ultima_cobranca = padrao.ultima_cobranca
    data_inicio = ultima_cobranca.data_geracao + timedelta(days=1) if ultima_cobranca else padrao.data_geracao
    data_fim = date.today() if not padrao.data_fim else min(date.today(), padrao.data_fim) 

    dias = []
    cobrancas_criadas = []

    if padrao.periodo == "anual" and data_inicio.year < data_fim.year:
        dias = rrule(YEARLY,dtstart=data_inicio, until=data_fim, bymonth=padrao.dia_cobranca, bymonthday=1)
    elif padrao.periodo == "mensal" and data_inicio < data_fim:
        dias = rrule(MONTHLY,dtstart=data_inicio, until=data_fim, bysetpos=padrao.dia_cobranca, byweekday=(MO,TU,WE,TH,FR))
    elif padrao.periodo == "semanal":
        dias = rrule(WEEKLY,dtstart=data_inicio, until=data_fim, wkst=MO, byweekday=calc_weekday(5))
    else:
        return []
    
    for dia in dias:
        mov = Movimentacao(descricao=padrao.descricao, valor_esperado=padrao.valor, data_geracao=dia, cod_usuario=padrao.cod_usuario, cod_categoria=padrao.cod_categoria, cod_padrao=padrao)
        cobrancas_criadas.append(mov)
    
    if create:
        return Movimentacao.objects.bulk_create(cobrancas_criadas) or []
    else:
        return cobrancas_criadas

def gera_cobrancas_pendentes(user, create=True):
    padroes = PadraoMovimentacao.objects.filter(cod_usuario=user)
    criadas = []
    for padrao in padroes:
        criadas = criadas + gerar_cobranca(padrao, False)
    
    if create:
        return Movimentacao.objects.bulk_create(criadas) or []
    else:
        return criadas

class CobrancaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user

        gera_cobrancas_pendentes(usuario)

        # Cobranças são movimentações geradas por padrões
        query = Movimentacao.objects.filter(cod_usuario=usuario, cod_padrao__isnull=False)


        validacao = FiltrarCobrancaSerializer(data=request.GET)
        validacao.is_valid(raise_exception=True)
        data = validacao.validated_data

        if "situacao" in data:
            situacao = data["situacao"]

            if situacao == "paga":
                query = query.filter(data_lancamento__isnull=False)
            elif situacao == "pendente":
                query = query.filter(data_lancamento__isnull=True)
            # elif situacao == "...":
        if "tipo" in data:
            query = query.filter(cod_padrao__receita_despesa=data["tipo"])
        if "cod_padrao" in data:
            query = query.filter(cod_padrao=data["cod_padrao"])

        # Converte queryset em uma lista de dicionarios(objetos)
        query = query.annotate(situacao=Case(
            When(data_lancamento__isnull=False, then=Value("paga")),
            When(data_lancamento__isnull=True, then=Value("pendente")),
            output_field=CharField()
        ))
        query = query.order_by("-data_geracao", "-data_lancamento")
        lista = query.values("id", "descricao", "valor_esperado", "data_geracao", "situacao", "cod_padrao", categoria=F("cod_categoria__nome"))
        lista = list(lista)

        return RespostaLista(200, lista)

class PagarPadraoView(APIView): 
    permission_classes = [IsAuthenticated]

    def put(self,request,id):
        user = request.user
        query = Movimentacao.objects.filter(id=id, cod_usuario=user)

        if not query.exists():
            return RespostaStatus(400, "Cobranca inexistente!")

        mov = query.first()

        json_data = json.loads(request.body)

        required_params(json_data, ["valor_pago"])
        validacao = PagarCobrancaSerializer(data=json_data)
        validacao.is_valid(raise_exception=True)
        data = validacao.validated_data
        

        mov.valor_pago = data["valor_pago"]
        mov.data_lancamento = date.today()
        mov.save()

        dic = model_to_dict(mov, ["id", "cod_padrao","valor_esperado","valor_pago","data_geracao","data_lancamento","descricao"])
        dic["categoria"] = mov.cod_categoria.nome

        return RespostaConteudo(200, dic)      



# Divida

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def exibir_divida(divida):
    dic_divida = model_to_dict(divida, fields=["id", "credor", "valor_divida", "valor_pago", "juros", "juros_ativos", "juros_tipo"])
    dic_padrao = model_to_dict(divida.cod_padrao, fields=["periodo", "dia_cobranca", "data_geracao", "data_fim"])
    dic_padrao["categoria"] = divida.cod_padrao.cod_categoria.nome
    dic = merge_two_dicts(dic_divida, dic_padrao)
    return dic

class InserirDividaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = request.user
        json_data = json.loads(request.body)

        required_params(json_data, ["credor", "valor_divida", "periodo", "dia_cobranca", "categoria", "data_fim"])
        validacao = ParametroDividaSerializer(data=json_data)
        validacao.is_valid(raise_exception=True)
        data = validacao.validated_data
        
        #Divida 
        credor= data["credor"]
        valor_divida= data["valor_divida"]
        
        #Padrão
        tipo= "divida"
        descricao = credor
        periodo = data["periodo"]
        dia_cobranca = data["dia_cobranca"]
        data_fim = data["data_fim"]
        categoria = data["categoria"]

        padrao = PadraoMovimentacao(receita_despesa=tipo, descricao=descricao, periodo=periodo, dia_cobranca=dia_cobranca, data_fim=data_fim, cod_usuario=usuario, cod_categoria=categoria)
        divida = Divida(credor=credor, valor_divida=valor_divida)#cod_usuario=usuario

        if "valor_pago" in data:
            divida.valor_pago = data["valor_pago"]

        if "juros" in data:
            if "juros_tipo" in data and "juros_ativos" in data:
                divida.juros = data["juros"]
                divida.juros_tipo = data["juros_tipo"]
                divida.juros_ativos = data["juros_ativos"]
            else:
                return RespostaStatus(400, "Se informado o campo 'juros', obrigatóriamente devem ser informados os campos 'juros_tipo' e 'juros_ativos'!")
    
        padrao.save()
        divida.cod_padrao = padrao
        divida.save()

        return RespostaConteudo(200, exibir_divida(divida))

class DividaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        usuario = request.user
        query = Divida.objects.filter(id=id)

        if not (query.exists() and query.first().cod_padrao.cod_usuario==usuario):
            return RespostaStatus(400, "Divida inexistente!")
        
        divida = query.first()

        return RespostaConteudo(200, exibir_divida(divida))             
    
    def put(self,request,id):
        usuario=request.user

        query = Divida.objects.filter(id=id)
        if not (query.exists() and query.first().cod_padrao.cod_usuario==usuario):
            return RespostaStatus(400, "Divida inexistente!")

        divida = query.first()
        padrao = divida.cod_padrao

        json_data = json.loads(request.body)
        validacao = ParametroDividaSerializer(data=json_data)
        validacao.is_valid(raise_exception=True)
        data = validacao.validated_data

        if "credor" in data:
            credor = data["credor"]
            divida.credor = credor
            padrao.descricao = credor 

        if "valor_pago" in data:
            divida.valor_pago = data["valor_pago"]

        if "valor_divida" in data:
            divida.valor_divida = data["valor_divida"]

        # Juros ignorado, será adicionado após reunião a respeito
        
        if "periodo" in data:
            padrao.periodo = data["periodo"]

        if "valor" in data:
            padrao.valor = data["valor"]
   
        if "dia_cobranca" in data:
            padrao.dia_cobranca = data["dia_cobranca"]

        if "data_geracao" in data:
            padrao.data_geracao = data["data_geracao"]

        if "data_fim" in data:
            padrao.data_fim = data["data_fim"]

        if "categoria" in data:
            categoria = data["categoria"]
            padrao.cod_categoria= cod_categoria

        divida.save()
        padrao.save()
            
        return RespostaConteudo(200,exibir_divida(divida))    

    def delete(self,request,id):
        usuario=request.user

        query = Divida.objects.filter(id=id)
        if not (query.exists() and query.first().cod_padrao.cod_usuario==usuario):
            return RespostaStatus(400, "Divida inexistente!")

        divida = query.first()
        padrao = divida.cod_padrao

        divida.delete()
        padrao.delete()
        return RespostaStatus(200,"Divida deletada!")     

class FiltrarDividasView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get (self,request):
        usuario = request.user
       
        validacao = FiltrarDividaSerializer(data=request.GET)
        validacao.is_valid(raise_exception=True)
        data = validacao.validated_data

        query_padrao = PadraoMovimentacao.objects.filter(receita_despesa='divida',cod_usuario=usuario)

        if "categoria" in data:
            query_padrao = query_padrao.filter(cod_categoria__nome=data["categoria"])
        
        query_divida = Divida.objects.filter(cod_padrao__in=query_padrao)

        if "juros_tipo" in data:
            query_divida =  query_divida.filter(juros_tipo=data["juros_tipo"])  
                                  
        if "juros_ativos" in request.GET:
            query_divida = query_divida.filter(juros_ativos=data["juros_ativos"])                

        if "quitada" in request.GET:
            if data["quitada"]:
                query_divida = query_divida.filter(valor_pago=F('valor_divida'))
            else:
                query_divida = query_divida.filter(valor_pago__lt=F('valor_divida'))    


        resultado = query_divida.values("id", "credor", "valor_divida", "valor_pago", "juros", "juros_ativos", "juros_tipo", 
        periodo=F("cod_padrao__periodo"), dia_cobranca=F("cod_padrao__dia_cobranca"), data_geracao=F("cod_padrao__data_geracao"), data_fim=F("cod_padrao__data_fim"))             
            
        return RespostaLista(200,list(resultado))     
