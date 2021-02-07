from .utils import *
from serase_app.models import *

from datetime import datetime, timedelta
from django.db.models import F, Sum, Q, FloatField, Count
from django.db.models import When, Case, Value, CharField
from django.db.models.functions import Coalesce, Extract, Cast

def analise_resumo(usuario, periodo):
    data_inicio, data_fim = calcula_periodo(periodo)
    
    query = Movimentacao.objects.filter(cod_usuario=usuario, data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)

    receita = float(query.filter(valor_pago__gte=0).aggregate(Sum("valor_pago"))["valor_pago__sum"] or 0.0)
    despesa = float(query.filter(valor_pago__lt=0).aggregate(Sum("valor_pago"))["valor_pago__sum"] or 0.0)
    total = receita + despesa

    return {
        "gasto_total": despesa,
        "receita_total": receita,
        "fluxo_total": total 
    }

def analise_categoria(usuario, periodo):
    data_inicio, data_fim = calcula_periodo(periodo)
    data_inicio_passado, data_fim_passado = calcula_periodo_anterior(periodo)

    categoria_ids = []

    # Seleciona despesas do usuario
    query = Movimentacao.objects.filter(cod_usuario=usuario, valor_pago__lt=0) 
    # Agrupa despesas por categoria
    query = query.values('cod_categoria')


    # 1- Calcular maior despesa

    # Seleciona despesas do periodo atual
    qperiodo_atual = query.filter(data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)
    # Soma todas as despesas de uma categoria em 'despesa_total' e ordena em ordem decrescente de despesa (maior despesa na frente)
    qperiodo_atual = qperiodo_atual.annotate(despesa_total=Sum('valor_pago')).order_by("despesa_total")

    if qperiodo_atual.count() > 0:
        cod_categ_despesa = qperiodo_atual.first()['cod_categoria']
        categoria_ids.append(cod_categ_despesa)
    else:
        cod_categ_despesa = None


    # 2 - Calcular maior salto/economia

    # Seleciona despesas entre o começo do ultimo periodo e o final do periodo atual
    qrelacao_ultimo = query.filter(data_lancamento__gte=data_inicio_passado, data_lancamento__lte=data_fim)
    
    # Cria atributo 'despesa_total', composta da soma das despesas do periodo atual menos a soma das despesas do ultimo periodo
    # Assim, 'despesa_total' é o valor a mais gasto em relação ao periodo passado. 
    # Ex: despesa_total: -700, significa que foi gasto +700 reais em relação ao mês passado
    #     despesa_total: +50, significa que foi gasto -50 reais em relação ao mês passado
    # Os sinais são invertidos pelo fato de uma movimentação de despesa possuir valores negativos.  
    qrelacao_ultimo = qrelacao_ultimo.annotate(
        despesa_total= Coalesce(Sum('valor_pago', filter=Q(data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)), 0.0) 
        - Coalesce(Sum('valor_pago', filter=Q(data_lancamento__gte=data_inicio_passado, data_lancamento__lte=data_fim_passado)),0.0)
    )

    # Ao ordernar temos no topo da lista o maior salto e no fim a maior economia
    qrelacao_ultimo = qrelacao_ultimo.order_by('despesa_total')

    if qrelacao_ultimo.count() > 0:
        cod_categ_salto = qrelacao_ultimo.first()['cod_categoria']
        cod_categ_economia = qrelacao_ultimo.last()['cod_categoria']
        categoria_ids.append(cod_categ_salto)
        categoria_ids.append(cod_categ_economia)
    else:
        cod_categ_salto = None
        cod_categ_economia = None

    
    # Pegar os nomes de cada categoria através de seus ids
    categorias = Categoria.objects.filter(id__in=categoria_ids)

    if qperiodo_atual.count() > 0:
        cod_categ_despesa = categorias.get(id=cod_categ_despesa).nome
    
    if qrelacao_ultimo.count() > 0:
        cod_categ_salto = categorias.get(id=cod_categ_salto).nome
        cod_categ_economia = categorias.get(id=cod_categ_economia).nome

    return {
        "maior_despesa": cod_categ_despesa,
        "maior_salto": cod_categ_salto,
        "maior_economia": cod_categ_economia,
    }

def grafico_semanal(usuario):
    data_inicio, data_fim = calcula_periodo("semanal")

    query = Movimentacao.objects.filter(cod_usuario=usuario, data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)
    query = query.annotate(dia=Extract("data_lancamento", "week_day")).values("dia")
    query = query.annotate(
        receita=Coalesce(Sum('valor_pago', filter=Q(valor_pago__gte=0)), 0.0),
        despesa=Coalesce(Sum('valor_pago', filter=Q(valor_pago__lt=0)), 0.0)
    ).values("dia","receita","despesa").order_by("dia")

    lista_dias_inclusos = list(query.values_list("dia", flat=True))
    resultado = list(query)

    for obj in resultado:
        obj['receita'] = round(obj['receita'], 2)
        obj['despesa'] = round(obj['despesa'], 2)

    for i in list(set(range(1,8)) - set(lista_dias_inclusos)):
        receita = 0.0
        despesa = 0.0
        resultado.append({"dia": i, "receita": receita, "despesa": despesa})

    return sorted(resultado, key=lambda k: k['dia'])

def grafico_categoria(usuario, periodo):
    data_inicio, data_fim = calcula_periodo(periodo, hoje)

    query = Movimentacao.objects.filter(cod_usuario=usuario, data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)
    query = query.filter(valor_pago__isnull=False)

    total_despesas = query.count()

    query = query.values(nome=F("cod_categoria__nome")).annotate(porcentagem=Cast(100.0 * Count("cod_categoria")/float(total_despesas), FloatField()))
    query = list(query)

    for obj in query:
        obj['porcentagem'] = round(obj['porcentagem'], 2)

    return query

def grafico_padrao_despesa(usuario, periodo):
    data_inicio, data_fim = calcula_periodo(periodo)

    query = Movimentacao.objects.filter(cod_usuario=usuario, data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)
    query = query.filter(cod_padrao__isnull=False, valor_pago__isnull=False, valor_pago__lt=0)

    query = query.annotate(tipo=Case(
        When(cod_padrao__valor__isnull=True, then=Value("Variáveis")),
        default=Value("Fixas"),
        output_field=CharField()
    ))

    total = query.count()

    query = query.values(nome=F("tipo")).annotate(porcentagem=Cast(100.0 * Count("tipo")/float(total), FloatField()))
    query = list(query)

    for obj in query:
        obj['porcentagem'] = round(obj['porcentagem'], 2)

    return query

def grafico_anual_despesa(usuario):
    usuario = User.objects.get(username="jv_eumsmo")

    hoje = datetime.strptime("2020-09-10", '%Y-%m-%d')
    periodo = "anual"
    data_inicio, data_fim = calcula_periodo(periodo, hoje)

    query = Movimentacao.objects.filter(cod_usuario=usuario, data_lancamento__gte=data_inicio, data_lancamento__lte=data_fim)
    query = query.filter(cod_padrao__isnull=False, valor_pago__isnull=False, valor_pago__lt=0, cod_padrao__valor__isnull=True)

    query = query.annotate(mes=Extract("data_lancamento", "month")).values("mes", nome=F("cod_padrao__descricao")).annotate(valor=Sum("valor_pago"))

    resultado = dict()
    query = list(query)

    # Formata o resultado para a resposta esperada
    for obj in query:
        valor = {"mes": obj["mes"], "valor": round(float(obj["valor"]), 2)}
        
        if obj["nome"] not in resultado:
            resultado[obj["nome"]] = list()
        resultado[obj["nome"]].append(valor)

    return resultado
def grafico_anual_saldo(usuario):
    usuario = User.objects.get(username="jv_eumsmo")
    hoje = datetime.strptime("2020-09-10", '%Y-%m-%d')
    ano= hoje.year
    query = Saldo.objects.filter(cod_usuario=usuario,mes_ano__year=ano)
    query= query.annotate(mes=Extract("mes_ano","month")).annotate(ano=Extract("mes_ano","year")).values("saldo","mes","ano")
    
    resultado = dict()
    query = list(query)
    # Formata o resultado para a resposta esperada
    for obj in query:
        valor = {"mes": obj["mes"], "saldo": round(float(obj["saldo"]), 2)}
        if obj["ano"] not in resultado:
            resultado[obj["ano"]] = list()
        resultado[obj["ano"]].append(valor)
    
        
    return resultado
    
def grafico_mensal_despesa(usuario):
    #dia e quantidade de despesas 
    usuario= User.objects.get(username="jv_eumsmo")
    hoje= get_hoje()
    mes_atual= hoje.month
    resultado = []

    query = Movimentacao.objects.filter(cod_usuario=usuario, data_lancamento__month=mes_atual)#filtrando movimentações relizadas no mes atual
    query = query.filter( valor_pago__isnull=False, valor_pago__lt=0)#filtrando despesas 
    query = query.annotate(dia=Extract("data_lancamento","day")).annotate(mes=Extract("data_lancamento","month"))
    query = query.values("dia","mes","data_lancamento")
   
    quantidade_de_despesas=[]
    dias_do_mes=[]
    queryLista = list(query)

    for obj in queryLista:#removendo dias duplicados
        if obj not in dias_do_mes:
            dias_do_mes.append(obj) 
    
    for obj in dias_do_mes:#contagem de despesas pagas  por dia
        qtd_aux=len(query.filter(data_lancamento__day=obj["dia"]))
        qtd_aux2={"quantidade":qtd_aux}
        quantidade_de_despesas.append(qtd_aux2)
    

    #formatação resposta
    for (d,q) in zip(dias_do_mes, quantidade_de_despesas):
        qtd= {"data":d["data_lancamento"],"quantidade":q["quantidade"]}
        resultado.append(qtd)
    return resultado
    
    
    
