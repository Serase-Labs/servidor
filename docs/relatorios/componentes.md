# Componentes
Os relatórios são compostos por múltiplos componentes. Desse modo, uma view pode retornar mais de um componente, porém todos os componentes possuem uma view que o retorna exclusivamente.

## Relatório Resumo
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


## Relatório Análises
Faz uma análise nas categorias das movimentações do período especificado. Para mais informações sobre uma categoria especifica, como as movimentações de tal categoria, procurar uma view base que retorna as informações necessárias, como a view de movimentações.

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

## Relatório Gráfico Semanal
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

## Relatório Gráfico Categoria
Retorna porcentagem de despesa por categoria do período especificado.

Recebe por parâmetro quantos valores exibir e quantos deixar em "Outros"

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

## Relatório Gráfico Padrão de Despesa
Retorna porcentagem de despesa por padrão de despesa do período especificado.

```
[
	{nome: "Fixas", porcentagem: 40},
	{nome: "Variaveis", porcentagem: 50},
	{nome: "Outros", porcentagem: 10}
]
```

## Relatório Gráfico Mensal de Despesa
Retorna quantidade de despesas de cada dia do mês.

```
[
	{ data: "2020-10-02", quantidade: 1},
	{ data: "2020-10-03", quantidade: 2},
	{ data: "2020-10-04", quantidade: 3},
	{ data: "2020-10-05", quantidade: 4}
]
```

## Relatório Gráfico Anual de Saldo
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

## Relatório Gráfico Anual de Despesa Fixa 
TO-DO