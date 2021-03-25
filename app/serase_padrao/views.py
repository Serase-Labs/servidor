# All Django Stuff
from django.db.models import F, Case, When, CharField, Value
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

# All rest framework stuff
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# All python and dependences stuff
from datetime import date
import json

# All in other app stuff
from serase_app.models import *
from serase_app.padroes_resposta import *



# Padrão

class InserirPadraoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = request.user
        json_data = json.loads(request.body)

        tipo= json_data["tipo"]
        descricao = json_data["descricao"]
        periodo = json_data["periodo"]
        valor =json_data["valor"]
        dia_cobranca = json_data["dia_cobranca"]
       # data_geracao  = json_data["data_geracao"]
        data_fim= json_data["data_fim"]
        categoria= json_data["categoria"]

        if Categoria.objects.filter(nome=categoria).exists():
            label = PadraoMovimentacao.objects.create(receita_despesa=tipo,descricao=descricao,periodo=periodo, valor=valor, dia_cobranca=dia_cobranca,data_fim=data_fim, cod_usuario=usuario,cod_categoria=Categoria.objects.get(nome=categoria))
            return RespostaConteudo(200, model_to_dict(label))
        else:
            return RespostaStatus(400, "Categoria Inexistente!")

class PadraoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        #Pegando o nome do usuário 
        usuario = request.user
        
        query = PadraoMovimentacao.objects.filter(cod_usuario=usuario,id=id)
        if query:
            lista = query.values("id", "descricao", "periodo", "dia_cobranca", "data_geracao", "data_fim", valor_padrao=F("valor"), categoria=F("cod_categoria__nome"), tipo=F("receita_despesa"))
            lista = list(lista)
            return RespostaConteudo(200,lista[0])             
        else:    
            return RespostaStatus(400,"Erro! esse id não está cadastrado")
     
    def put(self,request,id):
        usuario = request.user
        json_data = json.loads(request.body)
        query = PadraoMovimentacao.objects.get(id=id,cod_usuario=usuario)
        
        if "tipo" in json_data:
            tipo=json_data["tipo"]
            query.receita_despesa=tipo
            query.save()
        if "periodo" in json_data:
            periodo = json_data["periodo"]
            query.periodo=periodo
            query.save()
        if "descricao" in json_data:
            descricao = json_data["descricao"]
            query.descricao =descricao
            query.save()
        if "valor" in json_data:
            valor = json_data["valor"]
            query.valor =valor
            query.save()    
        if "dia_cobranca" in json_data:
            dia_cobranca = json_data["dia_cobranca"]
            query.dia_cobranca =dia_cobranca
            query.save()
        if "data_geracao" in json_data:
            data_geracao = json_data["data_geracao"]
            query.data_geracao =data_geracao
            query.save()    
        if "data_fim" in json_data:
            data_fim = json_data["data_fim"]
            query.data_fim = data_fim
            query.save()
        if "categoria" in json_data:
            categoria = json_data["categoria"]
            if Categoria.objects.filter(nome=categoria).exists():
                cod_categoria=Categoria.objects.get(nome=categoria)
                query.cod_categoria= cod_categoria
                query.save()
            else:
                return  RespostaStatus(400,"Erro! Categoria não existente") 
        return RespostaConteudo(200,model_to_dict(query))  
    
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
    permission_classes = [IsAuthenticated]

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
        lista = query.values("id", "descricao", "periodo", "dia_cobranca", "data_geracao", "data_fim", valor_padrao=F("valor"), categoria=F("cod_categoria__nome"), tipo=F("receita_despesa"))
        lista = list(lista)

        return RespostaLista(200, lista)



# Cobrança

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
        return Movimentacao.objects.bulk_create(cobrancas_criadas) or []
    else:
        return criadas

class CobrancaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        VALORES_VALIDOS_TIPO = ["receita", "despesa"]
        VALORES_VALIDOS_SITUACAO = ["pendente", "paga"]
        usuario = request.user

        gera_cobrancas_pendentes(usuario)

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

class PagarPadraoView(APIView): 
    permission_classes = [IsAuthenticated]

    def put(self,request,id):
        user =request.user
        query = Movimentacao.objects.get(id=id, cod_usuario=user)
        json_data = json.loads(request.body)
        if query:
            valor_pago = json_data["valor_pago"]
            data_lancamento  = date.today()
            query.valor_pago= valor_pago
            query.data_lancamento = data_lancamento
            query.save()

            return RespostaConteudo(200, model_to_dict(query))
        else:
            return RespostaStatus(400,"Erro! Esse id não existe")         



# Divida 

class InserirDividaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = request.user
        json_data = json.loads(request.body)
        
        #Divida 
        credor= json_data["credor"]
        valor_pago = json_data["valor_pago"]
        valor_divida= json_data["valor_divida"]
        juros = json_data["juros"]
        juros_tipo =json_data["juros_tipo"]
        juros_ativos = json_data["juros_ativos"]
        

        #Padrão da Divida  
        tipo= "divida"
    
        descricao = credor
        periodo = json_data["periodo"]
        dia_cobranca = json_data["dia_cobranca"]
       
        data_fim= json_data["data_fim"]
        categoria= json_data["categoria"]
    
        if Categoria.objects.filter(nome=categoria).exists():
            cod_padrao = PadraoMovimentacao.objects.create(receita_despesa=tipo,descricao=descricao,periodo=periodo, dia_cobranca=dia_cobranca,data_fim=data_fim, cod_usuario=usuario,cod_categoria=Categoria.objects.get(nome=categoria)).id
            CreateDivida=Divida.objects.create(credor=credor,valor_pago=valor_pago,valor_divida=valor_divida,juros=juros,juros_tipo=juros_tipo,juros_ativos=juros_ativos,cod_padrao= PadraoMovimentacao.objects.get(id=cod_padrao))
            return RespostaConteudo(200, model_to_dict(CreateDivida))
        else:
            return RespostaStatus(400, "Falha no Sistema")

class DividaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        usuario = request.user
        query = Divida.objects.filter(id=id)
        resultado=[]
        if query:
            codigo_padrao = Divida.objects.get(id=id).cod_padrao.id
            query_aux = PadraoMovimentacao.objects.filter(cod_usuario=usuario,id=codigo_padrao)
            lista_divida = query.values("id", "credor", "valor_pago", "valor_divida", "juros", "juros_tipo", "cod_padrao")
            lista_padrao= query_aux.values("periodo","dia_cobranca","data_geracao","data_fim","valor",categoria=F("cod_categoria__nome"))
            lista_divida = list(lista_divida)
            lista_padrao=list(lista_padrao)
           
            for (d,p) in zip(lista_divida, lista_padrao):
                aux= {"id":d["id"],"credor":d["credor"],"valor_pago":d["valor_pago"],"valor_divida":d["valor_divida"],"juros":d["juros"],"juros_tipo":d["juros_tipo"],"cod_padrao":d["cod_padrao"],\
                "periodo":p["periodo"],"dia_cobranca":p["dia_cobranca"],"data_geracao":p["data_geracao"],"data_fim":p["data_fim"],"valor":p["valor"], "categoria":p["categoria"]
                }
                resultado.append(aux)
            return RespostaConteudo(200,resultado)             
        else:    
            return RespostaStatus(400,"Erro! esse id não está cadastrado")
    
    def put(self,request,id):
        usuario=request.user
        query_divida = Divida.objects.get(id=id)
        json_data = json.loads(request.body)
        codigo_padrao = Divida.objects.get(id=id).cod_padrao.id
        query_padrao = PadraoMovimentacao.objects.get(cod_usuario=usuario,id=codigo_padrao)
        resultado=[]
        if query_divida:
            if "credor" in json_data:
                credor = json_data["credor"]
                query_divida.credor= credor
                query_padrao.descricao= credor 
                query_divida.save()
                query_padrao.save()
            if "valor_pago" in json_data:
                valor_pago = json_data["valor_pago"]
                query_divida.valor_pago=valor_pago
                query_divida.save()
                
            if "valor_divida" in json_data:
                valor_divida = json_data["valor_divida"]
                query_divida.valor_divida=valor_divida
                query_divida.save()    
                
            if "juros" in json_data:
                juros = json_data["juros"]
                query_divida.juros =juros
                query_divida.save()    
            
            if "juros_tipo" in json_data:
                juros_tipo = json_data["juros_tipo"]
                query_divida.juros_tipo =juros_tipo
                query_divida.save()    
                
            if "juros_ativos" in json_data:
                juros_ativos = json_data["juros_ativos"]
                query_divida.juros_ativos =juros_ativos 
                query_divida.save()    
        
            if "periodo" in json_data:
                periodo = json_data["periodo"]
                query_padrao.periodo=periodo
                query_padrao.save()

            if "valor" in json_data:
                valor = json_data["valor"]
                query_padrao.valor =valor
                query_padrao.save()    

            if "dia_cobranca" in json_data:
                dia_cobranca = json_data["dia_cobranca"]
                query_padrao.dia_cobranca =dia_cobranca
                query_padrao.save()

            if "data_geracao" in json_data:
                data_geracao= json_data["data_geracao"]
                query_padrao.data_geracao=data_geracao
                query_padrao.save()

            if "data_fim" in json_data:
                data_fim = json_data["data_fim"]
                query_padrao.data_fim = data_fim
                query_padrao.save()
            if "categoria" in json_data:
                categoria = json_data["categoria"]
                if Categoria.objects.filter(nome=categoria).exists():
                    cod_categoria=Categoria.objects.get(nome=categoria)
                    query_padrao.cod_categoria= cod_categoria
                    query_padrao.save()
                else:
                    return  RespostaStatus(400,"Erro! Categoria não existente") 
        else:
            return RespostaStatus(400,"Erro! esse id não está cadastrado")
        
            
        return RespostaConteudo(200,model_to_dict(query_divida))    

    def delete(self,request,id):
        usuario = request.user
        id_divida = id

        query = Divida.objects.filter(id=id)
        if query:
            codigo_padrao = Divida.objects.get(id=id_divida).cod_padrao
            query_aux = Divida.objects.get(id=id_divida).cod_padrao
            query.delete()
            query_aux.delete()
            return RespostaStatus(200,"Divida Deletada")             
        else:    
            return RespostaStatus(400,"Erro! Esse id não existe")   

class FiltrarDividasView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get (self,request):
        usuario = request.user
        lista_divida=[]
        resultado=[]
       
        query_padroes = PadraoMovimentacao.objects.filter(receita_despesa='divida',cod_usuario=usuario)
        if "categoria" in request.GET:
            categoria = request.GET["categoria"]
            if Categoria.objects.filter(nome=categoria).exists():
                 query_padroes = query_padroes.filter(cod_categoria__nome=categoria)          
            else:
                return  RespostaStatus(400,"Erro! Categoria não existente") 
        
        lista_padrao= query_padroes.values("id","periodo","dia_cobranca","data_geracao","data_fim","valor",categoria=F("cod_categoria__nome"))
       
        lista_padrao=list(lista_padrao)          
        
        
        for p in lista_padrao:
            id_padrao = p['id']
            query_aux = Divida.objects.filter(cod_padrao=id_padrao)
            query_aux=query_aux.values("id", "credor", "valor_pago", "valor_divida", "juros", "juros_tipo","juros_ativos")
            if "juros_tipo" in request.GET:
                tipo = request.GET["juros_tipo"]
                if tipo == "simples":
                    query_aux =  query_aux.filter(juros_tipo='simples')
                    
                elif tipo == "composto":
                    query_aux =  query_aux.filter(juros_tipo='composto')                
                else:
                    return RespostaAtributoInvalido("tipo", tipo, ["simples", "composto"])
            if "juros_ativos" in request.GET:
                juros_ativos = request.GET["juros_ativos"]
                if juros_ativos == True :
                    query_aux =  query_aux.filter(juros_ativos=True)
                    
                elif juros_ativos == False:
                    query_aux =  query_aux.filter(juros_ativos= False)                
                else:
                    return RespostaAtributoInvalido("juros_ativos", juros_ativos, [True,False])
            if "paga" in request.GET:
                paga= request.GET["paga"]
                if paga == True :
                    query_aux =  query_aux.filter(valor_pago=F('valor_divida'))
                elif paga == False:
                    query_aux =  query_aux.filter(valor_pago__lt=F('valor_divida'))    
                else:
                    return RespostaAtributoInvalido("paga", paga, [True,False])
            if query_aux:
                d= list(query_aux)
                aux= {"id":d[0]["id"],"credor":d[0]["credor"],"valor_pago":d[0]["valor_pago"],"valor_divida":d[0]["valor_divida"],"juros":d[0]["juros"],"juros_tipo":d[0]["juros_tipo"],"juros_ativos":d[0]["juros_ativos"],\
                "periodo":p["periodo"],"dia_cobranca":p["dia_cobranca"],"data_geracao":p["data_geracao"],"data_fim":p["data_fim"],"valor":p["valor"], "categoria":p["categoria"]}
            
                resultado.append(aux)
            
                  
            
        return RespostaConteudo(200,resultado)     

