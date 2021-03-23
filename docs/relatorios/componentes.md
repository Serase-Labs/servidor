# 🧩 Componentes
Os relatórios são compostos por múltiplos componentes. Desse modo, uma view pode retornar mais de um componente. Mesmo assim, todos os componentes possuem uma View que o retorna exclusivamente.

Ao chamar um relatório, os parâmetros serão definidos automaticamente pelo relatório, então não há com o que se preocupar. Porém se for necessário chamar apenas um componente, seus parâmetros devem ser passados na chamada.

Todos componentes são chamados com método GET.
| Caminho | Utilização | Incluso em Relatório |
|--|--|--|
|[/analise/resumo/{periodo}/](#análise-resumo)| Resumo das movimentações de um determinado período. | *Todos*
|[/analise/categoria/{periodo}/](#análise-categoria)| Informa quais categorias se destacaram em um determinado período.| *Todos*
|[/grafico/semanal/](#gráfico-semanal)| Retorna o total de receita e despesa realizada a cada dia de uma semana.|*Semanal*
|[/grafico/categoria/{periodo}/](#gráfico-geral-de-categoria)| Informa a porcentagem de gastos em cada categoria de um determinado período.|*Nenhum*
|[/grafico/padrao/{periodo}/](#gráfico-geral-de-padrão-de-despesa)| Informa a porcentagem de gastos em despesas fixas constantes ou variadas.|*Nenhum*
|[/grafico/despesa/mensal/](#gráfico-mensal-de-despesa)| Informa a quantidade de despesas feitas por dia do mês.|*Nenhum*
|[/grafico/despesa/anual/](#gráfico-anual-de-despesa-fixa)| Informa a variação do valor de despesas fixas variadas no ano.|*Anual*
|[/grafico/saldo/anual/](#gráfico-anual-de-saldo)| Informa o saldo de cada mês no ano.|*Anual*

# 🔬 Análises
Uma análise retorna informações que compõe um relatório.  As análises geralmente são gerais e recebem como parâmetro o período o qual será analisado.

## Análise Resumo

**URL:** `/analise/resumo/{periodo}/`

| parâmetro | valor |
|--|--|
| periodo | Aceita: "semanal", "mensal" e "anual" |

Retorna um resumo das movimentações do período especificado.

Informações do resumo:
- **Gasto Total:** Soma dos valores de todas as despesas do período.
- **Receita Total:** Soma dos valores de todas as receitas do período.
- **Fluxo Total:** Soma feita com os outros dois valores.

```
{
	gasto_total: -5.5,
	receita_total: 156.7,
	fluxo_total: 151.2
}
```


## Análise Categoria

**URL:** `/analise/categoria/{periodo}/`

| parâmetro | valor |
|--|--|
| periodo | Aceita: "semanal", "mensal" e "anual" |

Faz uma análise nas categorias das movimentações do período especificado. 

Informações da análise:
- **Maior despesa:** A categoria com maior valor de despesa no período.
- **Maior salto:** A categoria que apresentou maior aumento em despesa desde o ultimo período.
- **Maior economia:** A categoria que apresentou maior decréscimo em despesa desde o ultimo período.

```
{
	maior_despesa: "Lazer",
	maior_salto: "Alimentação",
	maior_economia: "Transporte"
}
```

# 📊 Gráficos
Gráficos são fundamentais para exibir informações em relatórios. Diferente das análises, a grande parte dos gráficos não são gerais, ou seja, são específicos para certo período e não possuindo variação de si para outros períodos.

## Gráfico Semanal

**URL:** `/grafico/semanal/`

Retorna informações importantes para gerar um gráfico com as informações das movimentações da semana

```
[
	{dia: 1, receita: 0, despesa: -350.5},
	{dia: 2, receita: 0, despesa: 0},
	{dia: 3, receita: 25.6, despesa: -7.9},
	{dia: 4, receita: 10, despesa: 0},
	{dia: 5, receita: 0, despesa: -500.6},
	{dia: 6, receita: 0, despesa: 0},
	{dia: 7, receita: 2365.5, despesa: 0}
]
```

## Gráfico Geral de Categoria

**URL:** `/grafico/categoria/{periodo}/`

| parâmetro | valor |
|--|--|
| periodo | Aceita: "semanal", "mensal" e "anual" |

Retorna porcentagem de despesa por categoria do período especificado.

```
[
	{nome: "Alimentação", porcentagem: 40},
	{nome: "Lazer", porcentagem: 32},
	{nome: "Compras", porcentagem: 12},
	{nome: "Moradia", porcentagem: 9},
	{nome: "Transporte", porcentagem: 5},
	{nome: "Outros", porcentagem: 2}
]
```

## Gráfico Geral de Padrão de Despesa

**URL:** `/grafico/padrao/{periodo}/`

| parâmetro | valor |
|--|--|
| periodo | Aceita: "semana", "mes" e "ano" |

Retorna porcentagem de despesa por padrão de despesa do período especificado.

```
[
	{nome: "Fixas", porcentagem: 40},
	{nome: "Variaveis", porcentagem: 50},
	{nome: "Outros", porcentagem: 10}
]
```

## Gráfico Mensal de Despesa

**URL:** `/grafico/despesa/mensal/`

Retorna quantidade de despesas de cada dia do mês.

```
[
	{ data: "2020-10-02", quantidade: 1},
	{ data: "2020-10-03", quantidade: 2},
	{ data: "2020-10-04", quantidade: 3},
	{ data: "2020-10-05", quantidade: 4}
]
```

## Gráfico Anual de Despesa Fixa 

**URL:** `/grafico/despesa/anual/`

Retorna a variação de valor de cada despesa fixa no decorrer do ano.

```
{
	"Conta de Luz": [
		{mes: 1, valor: 576.2},
		{mes: 2, valor: 585.5},
		...
		{mes: 12, valor: 603.1},
	],
	"Telefone Fixo": [ ... ],
	...
}
```


## Gráfico Anual de Saldo

**URL:** `/grafico/saldo/anual/`

Retorna o saldo total de cada mês do ano.

```
[
	{mes: 1, valor: 576.2},
	{mes: 2, valor: 58.5},
	{mes: 3, valor: 2400.2},
	{mes: 4, valor: -916.9},
	{mes: 5, valor: 136.7},
	...
	{mes: 12, valor: 603.1},
]
```
